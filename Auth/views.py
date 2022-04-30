from django.shortcuts import render
from rest_framework import generics, mixins
from Project.Auth.serializers import LateEntrySerializer

# Create your views here.

class LateEntryView(generics.GenericAPIView,\
                mixins.CreateModelMixin,\
                mixins.ListModelMixin):
    serializer_class = LateEntrySerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
