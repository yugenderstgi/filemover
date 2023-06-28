from django.db import connections
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import (
    FilemoverAction,
    FilemoverJob,
    FilemoverJobActionEvent,
    FilemoverJobEvent,
)
from ..utils import (
    FilemoverActionFilter,
    FilemoverJobActionEventFilter,
    FilemoverJobEventFilter,
    FilemoverJobFilter,
    convert_dict_to_xml,
    convert_dicttoxml_CDATA,
)
from .serializers import (
    FilemoverActionSerializer,
    FilemoverJobActionEventSerializer,
    FilemoverJobEventSerializer,
    FilemoverJobSerializer,
)


class SchemaNamesViewSet(viewsets.ViewSet):
    """
    Viewset for retrieving and updating database schema names.

    Args:
        viewsets.ViewSet: The base viewset class provided by Django REST Framework.

    Returns:
        Response: The response containing the retrieved schema names or indicating a successful update.

    Attributes:
        current_schema (dict): The dictionary representing the current schema, with the default value set to {"key": "public"}.
    """

    current_schema = {"key": "public"}

    def list(self, request):
        """
        Retrieve a list of available schema names.

        Returns:
            Response: The response containing the schema names and the current schema.
        """
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT DISTINCT table_schema FROM information_schema.tables where table_name like 'fm_job'")
            schema_names = [row[0] for row in cursor.fetchall()]
        return Response({"schema_names": schema_names, "current_schema": SchemaNamesViewSet.current_schema["key"]})

    def create(self, request):
        """
        Update the current database schema.

        Args:
            request (rest_framework.request.Request): The request object containing the selected schema name in the request data.

        Returns:
            Response: A response indicating a successful update of the database schema.
        """
        selected_schema = request.data.get("schema_name")

        SchemaNamesViewSet.current_schema["key"] = selected_schema

        db_settings = connections["default"].settings_dict
        db_settings["OPTIONS"]["options"] = f"-c search_path={selected_schema}"

        # Return a response indicating successful update
        return Response("Database schema updated successfully.")


class FilemoverJobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retrieving read-only file mover jobs.

    Args:
        viewsets.ReadOnlyModelViewSet: The base viewset class provided by Django REST Framework.

    Attributes:
        queryset (django.db.models.QuerySet): The queryset of FilemoverJob instances, ordered by descending dml_ts.
        serializer_class (serializers.Serializer): The serializer class used for serializing FilemoverJob instances.
        filter_backends (list): The list of filter backends to be applied for filtering the queryset. In this case,
                                DjangoFilterBackend is added to the list.
        filterset_class (type): The filterset class used for filtering the queryset.
        pagination_class (type): The pagination class used for pagination of the results.
    """

    queryset = FilemoverJob.objects.all().order_by("-dml_ts")
    serializer_class = FilemoverJobSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # this line to specify the filter backend and the DjangoFilterBackend is added to the filter_backends list
    filterset_class = FilemoverJobFilter
    # pagination_class = CustomPagination -> we  can use pagination from django-lc-utils/paginator.py


class FilemoverActionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retrieving read-only filemover actions.
    Attributes:
        queryset (django.db.models.QuerySet): The queryset of FilemoverActions instances, ordered by descending dml_ts.
    """

    queryset = FilemoverAction.objects.all().order_by("-dml_ts")
    serializer_class = FilemoverActionSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # this line to specify the filter backend and the DjangoFilterBackend is added to the filter_backends list
    filterset_class = FilemoverActionFilter

    @action(detail=True, methods=["PUT", "PATCH"])
    def action_params(self, request, pk=None):
        """
        This method is called to updated Action Params Values.
        """
        fm_action = self.get_object()
        fm_action_data = FilemoverActionSerializer(fm_action).data

        params = request.data.get("action_parms", {}).get("params", {})
        action_params = fm_action_data.get("action_parms")
        action_parms_xml = ""
        if fm_action.action_type == "Unzip" and params:
            action_params.update({"params": params})
            action_parms_xml = convert_dict_to_xml(action_params)
        else:
            transform_params = params.get("transform_params", {})
            # it fetches the value of the transform_params field
            if transform_params:
                params = action_params.get("params", {})
                params.update({"transform_params": transform_params})
                action_params.update({"params": params})
                # Change Action params back to XML
                action_parms_xml = convert_dicttoxml_CDATA(action_params)  # It includes CDATA in xml conversion

        fm_action.action_parms = action_parms_xml
        fm_action.save()
        serializer = self.get_serializer(
            fm_action
        )  # converting the FmAction instance into a serialized representation (e.g., JSON).
        return Response(serializer.data)  # response containing the serialized data of the FmAction instance.


class FilemoverJobEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retrieving read-only filemover Job Events.
    Attributes:
        queryset (django.db.models.QuerySet): The queryset of FilemoverJobEvent instances, ordered by descending start_tms.
    """

    queryset = FilemoverJobEvent.objects.all().order_by("-start_tms")
    serializer_class = FilemoverJobEventSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # this line to specify the filter backend and the DjangoFilterBackend is added to the filter_backends list
    filterset_class = FilemoverJobEventFilter


class FilemoverJobActionEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retrieving read-only filemover Job Action Events.
    Attributes:
        queryset (django.db.models.QuerySet): The queryset of FilemoverJobActionEvent instances, ordered by descending start_tms.
    """

    queryset = FilemoverJobActionEvent.objects.all().order_by("-start_tms")
    serializer_class = FilemoverJobActionEventSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # this line to specify the filter backend and the DjangoFilterBackend is added to the filter_backends list
    filterset_class = FilemoverJobActionEventFilter
