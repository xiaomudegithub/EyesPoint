from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ItemModel(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=150)
    rank = models.FloatField(default=0)
    userId = models.IntegerField(default=0)
    isFinished = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)


