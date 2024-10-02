from django.urls import path
from .views import *


app_name='rassilka'

urlpatterns= [
    path('', AppointmentView.as_view(), name='appointment'),
]