from django.contrib import admin
from api_space.models import *

# Register your models here.
admin.site.register(Country)
admin.site.register(ObjectType)
admin.site.register(Launch)
admin.site.register(SpaceTrack)

admin.site.register(Done)