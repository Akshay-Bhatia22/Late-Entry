from dataclasses import field
from rest_framework import serializers
from Core.models import *

class LateEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = LateEntry
        fields = ['__all__']