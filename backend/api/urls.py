from django.urls import include, path
from rest_framework import routers

from . import views

from .views import (
    FilemoverActionViewSet,
    FilemoverJobActionEventViewSet,
    FilemoverJobEventViewSet,
    FilemoverJobViewSet,
   
)

router = routers.DefaultRouter()
router.register(r"fmjobs", FilemoverJobViewSet, basename="fmjobs")
router.register(r"fmaction", FilemoverActionViewSet, basename="fmaction")
router.register(r"fmjobevent", FilemoverJobEventViewSet, basename="fmjobevent")
router.register(r"fmjobactionevent", FilemoverJobActionEventViewSet, basename="fmjobactionevent")

# router.register(r'fmjobs/fmaction', FmActionViewSet, basename='fmjobs-fmaction')

urlpatterns = [
    path("", include(router.urls)),
    path('schema-names/', views.SchemaNamesViewSet.as_view({'get': 'list', 'post': 'create'}), name='schema-names-list-create'),
   
]

# path('api/<str:schema_name>/',FmJobViewSet.as_view()),
