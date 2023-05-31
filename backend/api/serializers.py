from rest_framework import serializers
from .models import FmJob , FmAction , FmJobEvent ,FmJobActionEvent
import xmltodict
import xml.etree.ElementTree as ET
from .helpers import xml_to_json
import json


class FmJobSerailizer(serializers.ModelSerializer):
   
    class Meta:
        model = FmJob
        fields = ['id', 'name', 'dml_ts']

    
class FmActionSerailizer(serializers.ModelSerializer):
    transform_name= serializers.SerializerMethodField()
    action_parms = serializers.SerializerMethodField()
    class Meta:
        model=FmAction
        fields=['id','transform_name','seq','action_type','action_parms','dml_ts','description']
        # exclude=['fm_job_id']
    
    def get_action_parms(self,obj):
        xml_data = obj.action_parms
        dict_data = xmltodict.parse(xml_data)
        if obj.action_type=='Unzip':
            return dict_data
        transform_params = dict_data['params']['transform_params']
        if transform_params:
            # Preprocess the transform_params XML content
            preprocess_xml = f"<root>{transform_params}</root>"

            # Parse the preprocessed XML content
            parsed_data = xmltodict.parse(preprocess_xml)

            # Extract the transformed parameters
            transform_params = parsed_data['root']
        
        dict_data['params']['transform_params'] = transform_params
        return dict_data
    
    
     # if transform_params:
        #     transform_params = xmltodict.parse(transform_params) //The xmltodict.parse() method cannot handle multi-line XML content with multiple elements directly. 
                                                       #To parse such XML content, we  can preprocess it by wrapping it with a root element and then parse it using xmltodict.
        #     print("$$$",transform_params)


    

    def get_transform_name(self,obj):
        if obj.action_parms:
            try:
                root = ET.fromstring(obj.action_parms)
                transform_name = root.find('transform_name').text
                return transform_name
            except (ET.ParseError, AttributeError):
                pass
        return None
    

class FmJobEventSerailizer(serializers.ModelSerializer):

    job_name= serializers.ReadOnlyField(source='fm_job_id.name')
    job_duration = serializers.SerializerMethodField()
    class Meta:
        model=FmJobEvent
        fields=['id','fm_job_id','job_name','job_duration','start_tms','end_tms','status','src_ip']

    def get_job_duration(self, obj):
        duration = obj.end_tms - obj.start_tms
        return str(duration)
    
class FmJobActionEventSerailizer(serializers.ModelSerializer):
    transform_name= serializers.SerializerMethodField()
    seq=serializers.ReadOnlyField(source='fm_action_id.seq')
    action_type=serializers.ReadOnlyField(source='fm_action_id.action_type')
    action_duration = serializers.SerializerMethodField()
    resolved_action_parms = serializers.SerializerMethodField()
    class Meta:
        model=FmJobActionEvent
        fields=['id','fm_action_id','transform_name','seq','action_type','action_duration','start_tms','end_tms','status','resolved_action_parms']
    
    def get_action_duration(self, obj):
        duration = obj.end_tms - obj.start_tms
        return str(duration)
    
    def get_resolved_action_parms(self,obj):
        xml_data = obj.resolved_action_parms
        dict_data = xmltodict.parse(xml_data)
        # if obj.fm_action_id.action_type=='Unzip':
        #     return dict_data
        transform_params = dict_data['params']['transform_params']
        if transform_params:
            # Preprocess the transform_params XML content
            preprocess_xml = f"<root>{transform_params}</root>"

            # Parse the preprocessed XML content
            parsed_data = xmltodict.parse(preprocess_xml)

            # Extract the transformed parameters
            transform_params = parsed_data['root']
        
        dict_data['params']['transform_params'] = transform_params
        return dict_data
    
    def get_transform_name(self,obj):
        if obj.resolved_action_parms:
            try:
                root = ET.fromstring(obj.resolved_action_parms)
                transform_name = root.find('transform_name').text
                return transform_name
            except (ET.ParseError, AttributeError):
                pass
        return None
    
    


    

