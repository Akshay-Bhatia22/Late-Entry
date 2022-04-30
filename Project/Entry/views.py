from django.http.response import Http404
from rest_framework import mixins, status, generics
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

# ---------Serializers--------
from .serializers import LateEntrySerializer


class Scan(generics.CreateAPIView):

    serializer_class = LateEntrySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)