from django.urls import path
from . import views

urlpatterns = [
    path('scan', views.Scan.as_view()),
    path('manual',views.ManualEntry.as_view()),
    path('record',views.Record.as_view()),

]