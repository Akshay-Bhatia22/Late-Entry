from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.urls.conf import include
from Core.admin import staff_login
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/', staff_login.urls),
    path('auth/', include('Auth.urls')),
    path('entry/', include('Core.urls')),
    path('filer/', include('filer.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
