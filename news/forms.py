from django import forms
from .models import *

class Newsforms(forms.ModelForm):
    class Meta:
        model=Post
        fields=[
            'title',
            'text',
            'categories',

        ]