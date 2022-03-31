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
        fields = ('type',)


class SpaceTrackSerializer(serializers.ModelSerializer):

    country_code = serializers.StringRelatedField(source='country_code.code')
    object_type = ObjectTypeSerializer()
    launch = LaunchSerializer()

    def validate(self, attrs):
        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country_code'] = representation['country_code'].upper()
        return representation

    class Meta:
        model = SpaceTrack
        fields = '__all__'
