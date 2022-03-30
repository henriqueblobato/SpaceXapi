from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from api_space.models import SpaceTrack
from api_space.serializers import SpaceTrackSerializer


class SpaceTrackViewSet(viewsets.ModelViewSet):
    queryset = SpaceTrack.objects.all()
    serializer_class = SpaceTrackSerializer
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    # django-filters: is a django app that allows you to filter your queryset
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name', 'description',)

