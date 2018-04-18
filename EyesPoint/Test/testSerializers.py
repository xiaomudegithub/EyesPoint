#!/usr/bin/env python
# coding=utf-8

from Test.models import TestObject
from rest_framework import serializers

class TestObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestObject
        fields = "__all__"

    
