import logging

from rest_framework import serializers

from .models import (
    FilemoverAction,
    FilemoverJob,
    FilemoverJobActionEvent,
    FilemoverJobEvent,
)
from .utils import action_parms_val, transform_name_val

LOGGER = logging.getLogger("root")


class FilemoverJobSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """

    class Meta:
        model = FilemoverJob
        fields = ["id", "name", "description", "dml_ts"]


class FilemoverActionSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """

    transform_name = serializers.SerializerMethodField()
    action_parms = serializers.SerializerMethodField()

    class Meta:
        model = FilemoverAction
        fields = [
            "id",
            "transform_name",
            "seq",
            "action_type",
            "action_parms",
            "dml_ts",
            "description",
            "precondition_env",
        ]
        # exclude=['fm_job_id']

    def get_action_parms(self, instance):
        """
        This method converts action_parms from  XML format to nested dictionary
        """
        xml_data = instance.action_parms
        type = instance.action_type
        dict_data = action_parms_val(xml_data, type)
        return dict_data

    def get_transform_name(self, obj):
        """
        This method  returns transform_name  from action_parms
        """
        name = transform_name_val(obj.action_parms)
        return name


class FilemoverJobEventSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """

    job_name = serializers.ReadOnlyField(source="fm_job.name")
    job_duration = serializers.SerializerMethodField()

    class Meta:
        model = FilemoverJobEvent
        fields = ["id", "fm_job_id", "job_name", "job_duration", "start_tms", "end_tms", "status", "src_ip"]

    def get_job_duration(self, obj):
        """
        calculates job duration between start time and end time
        """
        job_duration = obj.end_tms - obj.start_tms
        return str(job_duration)


class FilemoverJobActionEventSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """

    transform_name = serializers.SerializerMethodField()
    seq = serializers.ReadOnlyField(source="fm_action_id.seq")
    action_type = serializers.ReadOnlyField(source="fm_action_id.action_type")
    action_duration = serializers.SerializerMethodField()
    resolved_action_parms = serializers.SerializerMethodField()

    class Meta:
        model = FilemoverJobActionEvent
        fields = [
            "id",
            "fm_action_id",
            "transform_name",
            "seq",
            "action_type",
            "action_duration",
            "start_tms",
            "end_tms",
            "status",
            "resolved_action_parms",
        ]

    def get_action_duration(self, obj):
        """
        get action duration
        """
        action_duration = obj.end_tms - obj.start_tms
        return str(action_duration)

    def get_resolved_action_parms(self, instance):
        """
        get resolved action params
        """
        xml_data = instance.resolved_action_parms
        type = instance.fm_action.action_type
        dict_data = action_parms_val(xml_data, type)
        return dict_data

    def get_transform_name(self, obj):
        """
        This method  returns transform_name  from resolved_action_parms
        """
        name = transform_name_val(obj.resolved_action_parms)
        return name
