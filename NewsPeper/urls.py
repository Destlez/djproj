from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('pages/', include('django.contrib.flatpages.urls')),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('sign/', include('sign.urls')),
    path('', include('protect.urls')),
    path('accounts/', include('allauth.urls')),
    path('appointment/', include('appointment.urls')),
]
