from uuid import uuid4

from django.db import models

# Create your models here.
# - spaceTrack.creation_date (represents the time that the lat/lon records were recorded)
# - longitude
# - latitude
# - id (this is the starlink satellite id)
# Goal: Query the last known position for a given satellite.


class Done(models.Model):
    file_mapped = models.BooleanField(default=False)

    def __str__(self):
        return self.file_mapped

    def __repr__(self):
        return self.file_mapped


class Country(models.Model):
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.code


class ObjectType(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type


class Launch(models.Model):
    id = models.AutoField(primary_key=True)
    launch_id = models.CharField(max_length=20)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class SpaceTrack(models.Model):
    primary_key = models.AutoField(primary_key=True)
    identifier = models.CharField(
        max_length=50,
        default=str(uuid4),
        editable=False,
    )
    object_name = models.CharField(max_length=100)
    creation_date = models.DateTimeField()
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    height_km = models.FloatField(null=True, blank=True)
    country_code = models.ForeignKey(Country, on_delete=models.CASCADE)
    object_type = models.ForeignKey(ObjectType, on_delete=models.CASCADE)

    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
