from django.db import models
from django.contrib.auth.models import User

class Christian(models.Model):
    name = models.CharField(max_length=100, null=False, default="John Doe")
    age = models.IntegerField(null=False, default=18)
    gender = models.CharField(max_length=6, null=False, default='Custom')
    role = models.CharField(max_length=100, null=False, default='Christian')
    status = models.CharField(max_length=100, null=False, default='Single')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
