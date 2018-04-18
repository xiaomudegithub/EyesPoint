from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TestObject(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
