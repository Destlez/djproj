from email.policy import default

from django.db import models
from datetime import datetime

class Appointment(models.Model):
    date = models.DateTimeField(
        auto_now_add=True
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'