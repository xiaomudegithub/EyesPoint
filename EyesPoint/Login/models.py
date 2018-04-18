from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length= 30)
    userEmail = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    accesstoken = models.CharField(max_length=100, default=None, null=True)

class ValidCode(models.Model):
    userEmail = models.CharField(max_length=100)
    valCode = models.CharField(max_length=6)
    timestamp = models.CharField(max_length=20)
    accesstoken = models.CharField(max_length=100, default=None, null=True)




