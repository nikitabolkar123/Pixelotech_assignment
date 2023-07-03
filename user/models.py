from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    phone_no = models.IntegerField(default=0)
    location = models.CharField(max_length=200, null=True)
