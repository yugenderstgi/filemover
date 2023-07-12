import xmltodict
from django_filters import rest_framework as filters

from .models import (
    FilemoverAction,
    FilemoverJob,
    FilemoverJobActionEvent,
    FilemoverJobEvent,
)


class FilemoverJobFilter(filters.FilterSet):
    """
    This class is used to  filter based on  Job Name.
    Using a FilterSet class will make it easier to add more complex filters and
    provide a more organized way to handle filtering in API views.
    """

    job_name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = FilemoverJob
        fields = ["name"]


class FilemoverActionFilter(filters.FilterSet):
    """
    This class is used to  filter based on  Job id , Fm action id , Transform name.
    """

    fm_action_id = filters.NumberFilter(field_name="id", lookup_expr="exact")
    transform_name = filters.CharFilter(method="filter_by_transform_name")

    # custom filter method of the viewset to perform the filtering based on the serializer field.
    def filter_by_transform_name(self, queryset, transform_name, value):
        return queryset.filter(action_parms__icontains=value)

    class Meta:
        model = FilemoverAction
        fields = ["id", "action_type"]  # This fields related to Model Class


class FilemoverJobEventFilter(filters.FilterSet):
    """
    This class is used to  filter based on  Job name,Job Status , Date Range.
    """

    job_name = filters.CharFilter(field_name="fm_job__name", lookup_expr="icontains")
    status = filters.CharFilter(field_name="status", lookup_expr="icontains")

    class Meta:
        model = FilemoverJobEvent
        fields = ["status"]  # , "start_tms", "end_tms"]


class FilemoverJobActionEventFilter(filters.FilterSet):
    """
    This class is used to  filter based on   job action event id ,Job Status , Transform name.
    """

    fm_job_action_event_id = filters.NumberFilter(field_name="id", lookup_expr="exact")
    status = filters.CharFilter(field_name="status", lookup_expr="icontains")
    transform_name = filters.CharFilter(method="filter_by_transform_name")

    # custom filter method of the viewset to perform the filtering based on the serializer field.
    def filter_by_transform_name(self, queryset, transform_name, value):
        return queryset.filter(resolved_action_parms__icontains=value)

    class Meta:
        model = FilemoverJobActionEvent
        fields = ["id", "status"]  # This fields related to Model Class


def transform_name_val(xmldata):
    """
    This method converts action_params from xml to dict and it  returns transform_name  from action_parms.
    """
    try:
        if xmldata:
            dict_data = xmltodict.parse(xmldata)
            transform_name = dict_data.get("params", {}).get("transform_name")
            return transform_name
    except Exception as e:
        print(e)
        return None


def action_parms_val(xml_data, action_type):
    """
    This method  converts action_parms from xml to nested dict format
    """

    dict_data = xmltodict.parse(xml_data)

    if action_type == "Unzip":
        return dict_data
    transform_params = dict_data["params"]["transform_params"]

    # here if transform_params value is still not converted into dict then it goes to below if condition to convert it into dict
    if transform_params and isinstance(transform_params, str):
        # Preprocess the transform_params XML content
        preprocess_xml = f"<root>{transform_params}</root>"

        # Parse the preprocessed XML content
        parsed_data = xmltodict.parse(preprocess_xml)

        # Extract the transformed parameters
        transform_params = parsed_data["root"]

    if "#text" in transform_params:  # It remove "#text" key and its value from transform_params dict
        transform_params.pop("#text", None)
    dict_data["params"]["transform_params"] = transform_params

    return dict_data


def convert_dict_to_xml(data_dict):
    """
    Method to convert dict to xml where action_params does not have transform_params field and includes proper identation format
    """
    # data_dict = json.loads(data_string)

    xml_str = xmltodict.unparse(data_dict, pretty=True)
    xml_str = xml_str.replace('<?xml version="1.0" encoding="utf-8"?>', "")

    xml_str = xml_str.strip()  # Remove leading/trailing whitespace
    if xml_str.startswith("\n"):
        xml_str = xml_str[1:]  # Remove leading newline character
    return xml_str


def convert_dicttoxml_CDATA(data_dict):
    """
    This method converts dict to xml which includes CDATA in transform_params
    """

    temp = data_dict["params"]["transform_params"]

    xml_string = "\n\t\t".join(
        f"<{key}>{value}</{key}>" for key, value in temp.items()
    )  # Resulting strings are then concatenated using join() to create the final XML-like string
    updated_data = f"\t<transform_params>![CDATA[\n\t\t{xml_string}\n\t]]</transform_params>\n"

    data_dict["params"]["transform_params"] = updated_data
    modified_data = data_dict.copy()
    modified_data["params"].pop("transform_params")
    # Convert the dictionary to XML
    xml_data = convert_dict_to_xml(modified_data)
    # xml_data = xmltodict.unparse(modified_data,pretty=True)
    insert_index = xml_data.index("</params>")
    modified_xml_data = xml_data[:insert_index] + updated_data + xml_data[insert_index:]

    xml_data_str = str(modified_xml_data)

    return xml_data_str
