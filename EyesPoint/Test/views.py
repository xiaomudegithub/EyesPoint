from django.shortcuts import render
from models import TestObject
from rest_framework import viewsets
from testSerializers import TestObjectSerializer

# Create your views here.

class TestObjectViewSet(viewsets.ModelViewSet):
    queryset = TestObject.objects.all()
    serializer_class = TestObjectSerializer
