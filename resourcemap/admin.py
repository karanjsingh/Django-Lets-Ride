from django.contrib import admin

# Register your models here.
from .models import Requests,Rides

admin.site.register(Requests)
admin.site.register(Rides)