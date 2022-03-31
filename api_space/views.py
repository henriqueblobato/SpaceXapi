from math import radians, cos, sin, asin, sqrt

from rest_framework import viewsets
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
        ts = self.request.query_params.get('ts', None)
        identifier = self.request.query_params.get('identifier', None)
        coordinates = self.request.query_params.get('coordinates', None)

        queryset = self.queryset

        if ts:
            queryset = queryset.filter(creation_date__lte=ts)
        if object_name:
            queryset = queryset.filter(object_name__icontains=object_name)
        if country_code:
            queryset = queryset.filter(country_code__icontains=country_code)
        if identifier:
            queryset = queryset.filter(identifier__icontains=identifier)
        if coordinates:
            queryset = self.calculate_haversine(queryset, coordinates)
            return queryset

        return queryset.order_by('-creation_date')

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        if not all([lat1, lon1, lat2, lon2]):
            return None
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers is 6371
        km = 6371 * c
        km = round(km, 2)
        return km

    def calculate_haversine(self, queryset, coordinates):
        lat, lon = coordinates.split(',')
        lat, lon = float(lat), float(lon)
        tracks_dict = {}
        for tracks in queryset:
            haversine_result_km = self.haversine(tracks.latitude, tracks.longitude, lat, lon)
            if haversine_result_km:
                tracks_dict[tracks] = haversine_result_km

        sorted_tracks = dict(sorted(tracks_dict.items(), key=lambda item: item[1])[:10])
        return queryset.filter(object_name__in=list(sorted_tracks.keys()))


class LaunchViewSet(viewsets.ModelViewSet):
    queryset = Launch.objects.all()
    serializer_class = LaunchSerializer


class ObjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ObjectType.objects.all()
    serializer_class = ObjectTypeSerializer
