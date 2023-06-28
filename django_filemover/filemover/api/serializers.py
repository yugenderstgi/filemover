from rest_framework import serializers

from ..models import (
    FilemoverAction,
    FilemoverJob,
    FilemoverJobActionEvent,
    FilemoverJobEvent,
)
from ..utils import action_parms_val, transform_name_val


class FilemoverJobSerializer(serializers.ModelSerializer):
    """
    Serializer for the FilemoverJob model.

    Args:
        serializers.ModelSerializer: The base serializer class provided by Django REST Framework.

    Returns:
        dict: A dictionary representing the serialized FilemoverJob instance.
    """

    class Meta:
        model = FilemoverJob
        fields = ["id", "name", "description", "dml_ts"]


class FilemoverActionSerializer(serializers.ModelSerializer):
    """
    Serializer for the FilemoverAction model.

    Args:
        serializers.ModelSerializer: The base serializer class provided by Django REST Framework.

    Returns:
        dict: A dictionary representing the serialized FilemoverAction instance.
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
        This method converts action_parms from XML format to a nested dictionary.

        Args:
            instance (FilemoverAction): The FilemoverAction instance being serialized.

        Returns:
            dict: A nested dictionary representing the deserialized action_parms.
        """

        xml_data = instance.action_parms
        type = instance.action_type
        dict_data = action_parms_val(xml_data, type)
        return dict_data

    def get_transform_name(self, obj):
        """
        This method returns the transform_name from action_parms.

        Args:
            obj (FilemoverAction): The FilemoverAction instance being serialized.

        Returns:
            str: The transform_name extracted from the action_parms.
        """
        name = transform_name_val(obj.action_parms)
        return name


class FilemoverJobEventSerializer(serializers.ModelSerializer):
    """
    Serializer for the FilemoverJobEvent model.

        Args:
        serializers.ModelSerializer: The base serializer class provided by Django REST Framework.

    Returns:
        dict: A dictionary representing the serialized FilemoverJobEvent instance.
    """

    job_name = serializers.ReadOnlyField(source="fm_job.name")
    job_duration = serializers.SerializerMethodField()

    class Meta:
        model = FilemoverJobEvent
        fields = ["id", "fm_job_id", "job_name", "job_duration", "start_tms", "end_tms", "status", "src_ip"]

    def get_job_duration(self, obj):
        """
        Calculates the duration of a job based on the start time and end time.

        Args:
            obj: The instance of the job for which to calculate the duration.

        Returns:
            str: A string representation of the job duration.
        """
        job_duration = obj.end_tms - obj.start_tms
        return str(job_duration)


class FilemoverJobActionEventSerializer(serializers.ModelSerializer):
    """
    Serializer for the FilemoverJobActionEvent model.

        Args:
        serializers.ModelSerializer: The base serializer class provided by Django REST Framework.

    Returns:
        dict: A dictionary representing the serialized FilemoverJobActionEvent instance.
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
        Calculates the duration of a action based on the start time and end time.

        Args:
            obj: The instance of the action for which to calculate the duration.

        Returns:
            str: A string representation of the action duration.
        """
        action_duration = obj.end_tms - obj.start_tms
        return str(action_duration)

    def get_resolved_action_parms(self, instance):
        """
        This method converts resolved_action_parms from XML format to a nested dictionary.

        Args:
            instance (FilemoverJobActionEvent): The FilemoverJobActionEvent instance being serialized.

        Returns:
            dict: A nested dictionary representing the deserialized resolved_action_parms.
        """
        xml_data = instance.resolved_action_parms
        type = instance.fm_action.action_type
        dict_data = action_parms_val(xml_data, type)
        return dict_data

    def get_transform_name(self, obj):
        """
        This method returns the transform_name from resolved_action_parms.

        Args:
            obj (FilemoverAction): The FilemoverJobActionEvent instance being serialized.

        Returns:
            str: The transform_name extracted from the resolved_action_parms.
        """
        name = transform_name_val(obj.resolved_action_parms)
        return name
