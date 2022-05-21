from rest_framework import serializers
from Core.models import LateEntry
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Student, Venue
class LateEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = LateEntry
        fields = ['student']

class StudentRecordSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='late_entry_count')
    timestamp = serializers.DateTimeField(source='timestamp_entry')

    class Meta:
        model = Student
        fields = ['student_no','name','count','timestamp']


class StudentIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

class CacheSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ['id','venue']