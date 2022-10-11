from pyexpat import model
from attr import fields
from rest_framework import serializers
from .models import Lodging

class LodgingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lodging
        fields = '__all__'

class SimpleLodgingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lodging
        fields = ['id', 'lodging_name', 'lodging_address', 'lodging_img1']