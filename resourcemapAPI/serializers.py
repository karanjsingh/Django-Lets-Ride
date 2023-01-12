from rest_framework import serializers
from resourcemap.models import Requests,Rides

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rides
        fields = '__all__'