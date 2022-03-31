from typing import OrderedDict

from rest_framework import serializers

from api_space.models import SpaceTrack, Launch, ObjectType, Country


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

    def create(self, validated_data):
        obj_type = dict(validated_data['object_type']).get('type')
        if obj_type.isdigit():
            obj_id = obj_type
            object_type = ObjectType.objects.get(pk=obj_id)
            validated_data['object_type'] = object_type
        if isinstance(obj_type, str):
            object_type = ObjectType.objects.get(type=obj_type)
            validated_data['object_type'] = object_type

        if isinstance(validated_data['launch'], OrderedDict):
            launch_id = dict(validated_data['launch']).get('launch_id')
            launch, _ = Launch.objects.get_or_create(launch_id=launch_id)
            validated_data['launch'] = launch

        return SpaceTrack.objects.create(**validated_data)

    def validate(self, attrs):
        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country_code'] = representation['country_code'].upper()
        return representation

    class Meta:
        model = SpaceTrack
        fields = '__all__'
