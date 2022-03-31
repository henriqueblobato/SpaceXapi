from django.contrib import admin
from api_space.models import *

# Register your models here.
admin.register(Country)
admin.register(ObjectType)
admin.register(Launch)
admin.register(SpaceTrack)

admin.site.register(Done)