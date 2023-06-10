from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    FilemoverAction,
    FilemoverJob,
    FilemoverJobActionEvent,
    FilemoverJobEvent,
)
from .serializers import (
    FilemoverActionSerializer,
    FilemoverJobActionEventSerializer,
    FilemoverJobEventSerializer,
    FilemoverJobSerializer,
)
from .utils import (
    FilemoverActionFilter,
    FilemoverJobActionEventFilter,
    FilemoverJobEventFilter,
    FilemoverJobFilter,
    convert_dict_to_xml,
    convert_dicttoxml_CDATA,
)


class FilemoverJobViewSet(viewsets.ReadOnlyModelViewSet):
    """_summary_

    Args:
        viewsets (_type_): _description_
    """

    queryset = FilemoverJob.objects.all().order_by("-dml_ts")
    serializer_class = FilemoverJobSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # this line to specify the filter backend and the DjangoFilterBackend is added to the filter_backends list
    filterset_class = FilemoverJobFilter


class FilemoverActionViewSet(viewsets.ReadOnlyModelViewSet):
    """_summary_

    Args:
        viewsets (_type_): _description_

    Returns:
        _type_: _description_
    """

    queryset = FilemoverAction.objects.all().order_by("-dml_ts")
    serializer_class = FilemoverActionSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # this line to specify the filter backend and the DjangoFilterBackend is added to the filter_backends list
    filterset_class = FilemoverActionFilter

    @action(detail=True, methods=["PUT", "PATCH"])
    def update_action_params(self, request, pk=None):
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
    """_summary_

    Args:
        viewsets (_type_): _description_
    """

    queryset = FilemoverJobEvent.objects.all().order_by("-start_tms")
    serializer_class = FilemoverJobEventSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # this line to specify the filter backend and the DjangoFilterBackend is added to the filter_backends list
    filterset_class = FilemoverJobEventFilter


class FilemoverJobActionEventViewSet(viewsets.ReadOnlyModelViewSet):
    """_summary_

    Args:
        viewsets (_type_): _description_
    """

    queryset = FilemoverJobActionEvent.objects.all().order_by("-start_tms")
    serializer_class = FilemoverJobActionEventSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # this line to specify the filter backend and the DjangoFilterBackend is added to the filter_backends list
    filterset_class = FilemoverJobActionEventFilter
