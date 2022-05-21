from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.Scan.as_view()),
    path('bulk/',views.Bulk.as_view()),
    path('cache/',views.Cache.as_view()),
    path('venue/',views.GetVenue.as_view()),

]