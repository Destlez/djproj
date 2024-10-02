from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import *


class NewsFilter(FilterSet):
    created_at = DateFilter(
        field_name='created_at',
        widget=DateInput(attrs={'type':'date'}),
        label='date',
        lookup_expr='date__exact'
    )
    class Meta:
       model = Post
       fields = {
           'title': ['icontains'],
           'author': ['exact'],
       }