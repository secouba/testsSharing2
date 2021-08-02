from django.contrib import admin
from .models import Users, Resource, Booking


admin.site.register(Booking)
admin.site.register(Resource)
admin.site.register(Users)