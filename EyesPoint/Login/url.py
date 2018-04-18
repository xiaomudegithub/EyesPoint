#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'test/', test),
    url(r'testPost/',postTest),
    url(r'getValidCode/',getValidCode), 
    url(r'checkValidCode$', checkValidCode),
    url(r'registerOrUpdatepwd$', registerOrUpdatepwd),
    url(r'loginChecked', login),
]
