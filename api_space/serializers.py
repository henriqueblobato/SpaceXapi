from rest_framework import serializers

from api_space.models import SpaceTrack, Launch, ObjectType


class LaunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Launch
        fields = (
            'launch_id',
            'date',
        )


class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectType
        fields = '__all__'


class SpaceTrackSerializer(serializers.ModelSerializer):

    country_code = serializers.StringRelatedField(source='country_code.code')
    object_type = ObjectTypeSerializer().fields
    launch = LaunchSerializer()

    class Meta:
        model = SpaceTrack
        fields = '__all__'