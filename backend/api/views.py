from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .helpers import convert_dict_to_xml
from .models import FmAction, FmJob, FmJobActionEvent, FmJobEvent
from .serializers import (
    FmActionSerailizer,
    FmJobActionEventSerailizer,
    FmJobEventSerailizer,
    FmJobSerailizer,
)


class FmJobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FmJobSerailizer

    def get_queryset(self):
        queryset = FmJob.objects.all().order_by("-dml_ts")
        name = self.request.query_params.get("name", None)
        if name is not None:
            queryset = queryset.filter(Q(name__icontains=name))
        return queryset


class FmActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FmAction.objects.all()
    serializer_class = FmActionSerailizer

    def get_queryset(self):
        queryset = super().get_queryset()
        fm_job_id = self.request.query_params.get("fm_job_id", None)
        if fm_job_id:
            queryset = queryset.filter(fm_job_id=fm_job_id)
        transform_name = self.request.query_params.get("transform_name", None)
        id = self.request.query_params.get("id", None)
        if id:
            queryset = queryset.filter(id=id)
        if transform_name:
            queryset = queryset.filter(Q(action_parms__icontains=transform_name))
        action_type = self.request.query_params.get("action_type", None)
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        return queryset

    @action(detail=True, methods=["PUT", "PATCH"])
    def update_action_params(self, request, pk=None):
        fm_action = self.get_object()
        fm_action_data = FmActionSerailizer(fm_action).data

        params = request.data.get("action_parms", {}).get("params", {})
        action_params = fm_action_data.get("action_parms")
        if fm_action.action_type == "Unzip" and params:
            action_params.update({"params": params})
        else:
            transform_params = params.get("transform_params", {})
            # it fetches the value of the transform_params field

            if transform_params:
                params = action_params.get("params", {})
                params.update({"transform_params": transform_params})
                action_params.update({"params": params})

        # Change Action params back to XML
        fm_action_xml = convert_dict_to_xml(action_params)
        fm_action.action_parms = fm_action_xml
        fm_action.save()
        serializer = self.get_serializer(
            fm_action
        )  # converting the FmAction instance into a serialized representation (e.g., JSON).
        return Response(serializer.data)  # response containing the serialized data of the FmAction instance.


class FmJobEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FmJobEvent.objects.all().order_by("-start_tms")
    serializer_class = FmJobEventSerailizer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("job_name", None)
        if name is not None:
            queryset = queryset.filter(fm_job_id__name=name)

        status = self.request.query_params.get("status", None)
        if status is not None:
            queryset = queryset.filter(status=status)

        start_tms = self.request.query_params.get("start_tms", None)
        end_tms = self.request.query_params.get("end_tms", None)
        if start_tms and end_tms:
            queryset = queryset.filter(Q(start_tms__date__gte=start_tms) & Q(end_tms__date__lte=end_tms))

        return queryset


class FmJobActionEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FmJobActionEvent.objects.all()
    serializer_class = FmJobActionEventSerailizer

    def get_queryset(self):
        queryset = super().get_queryset()

        fm_job_event_id = self.request.query_params.get("fm_job_event_id", None)
        if fm_job_event_id:
            queryset = queryset.filter(fm_job_event_id=fm_job_event_id)

        transform_name = self.request.query_params.get("transform_name", None)
        if transform_name:
            queryset = queryset.filter(Q(resolved_action_parms__contains=transform_name))

        status = self.request.query_params.get("status", None)
        if status is not None:
            queryset = queryset.filter(status=status)

        return queryset


# Create your views here.
# Without ORM
# class FmJobViewSet(View):
#     def get(self,request,schema_name):
#         with SchemaDatabase(schema_name) as cursor:
#             cursor.execute("select * from fm_job")
#             result=cursor.fetchall()
#             columns = list(cursor.description)
#             results = []
#             for row in result:
#                 row_dict = {}
#                 for i, col in enumerate(columns):
#                     row_dict[col.name] = row[i]
#                 results.append(row_dict)

#         return JsonResponse(results, safe=False)
