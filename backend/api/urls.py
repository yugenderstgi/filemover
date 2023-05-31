from django.urls import include, path
from rest_framework import routers

from .views import (
    FmActionViewSet,
    FmJobActionEventViewSet,
    FmJobEventViewSet,
    FmJobViewSet,
)

router = routers.DefaultRouter()
router.register(r"fmjobs", FmJobViewSet, basename="fmjobs")
router.register(r"fmaction", FmActionViewSet, basename="fmaction")
router.register(r"fmjobevent", FmJobEventViewSet, basename="fmjobevent")
router.register(r"fmjobactionevent", FmJobActionEventViewSet, basename="fmjobactionevent")

# router.register(r'fmjobs/fmaction', FmActionViewSet, basename='fmjobs-fmaction')

urlpatterns = [
    path("", include(router.urls)),
]

# path('api/<str:schema_name>/',FmJobViewSet.as_view()),
