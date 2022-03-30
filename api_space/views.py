from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.templatetags import rest_framework
import django_filters.rest_framework

from api_space.models import (
    SpaceTrack,
    Launch,
    ObjectType
)
from api_space.serializers import (
    SpaceTrackSerializer,
    LaunchSerializer,
    ObjectTypeSerializer
)


class SpaceTrackViewSet(viewsets.ModelViewSet):
    queryset = SpaceTrack.objects.all()
    serializer_class = SpaceTrackSerializer

    def get_queryset(self):
        object_name = self.request.query_params.get('object_name', None)
        country_code = self.request.query_params.get('country_code', None)

        queryset = SpaceTrack.objects.all()

        if object_name is not None:
            queryset = queryset.filter(object_name__icontains=object_name)
        elif country_code is not None:
            queryset = queryset.filter(country_code__icontains=country_code)

        return queryset.order_by('-creation_date')


class LaunchViewSet(viewsets.ModelViewSet):
    queryset = Launch.objects.all()
    serializer_class = LaunchSerializer


class ObjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ObjectType.objects.all()
    serializer_class = ObjectTypeSerializer
