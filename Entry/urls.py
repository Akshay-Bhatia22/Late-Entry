from django.urls import path
from . import views

urlpatterns = [
    path('scan', views.Scan.as_view()),
]