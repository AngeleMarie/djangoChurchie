from django.db import models
from django.contrib.auth.models import User  # Ensure this import is present

class Event(models.Model):
    name = models.CharField(max_length=100,default='')
    location = models.CharField(max_length=100,default='')
    date = models.DateField(default='')
    description = models.TextField(default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=False)  # or another user model

    def __str__(self):
        return self.name
