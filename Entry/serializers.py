from rest_framework import serializers
from Core.models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class LateEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = LateEntry
        fields = ['__all__']
