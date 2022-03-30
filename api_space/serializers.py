from rest_framework import serializers

from api_space.models import SpaceTrack


class SpaceTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceTrack
        fields = '__all__'
