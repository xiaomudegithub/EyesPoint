#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'unfinishedItems/', unfinishedItems),
    url(r'historyItems/', historyItems),
    url(r'addItem/', addItem),
    url(r'deleteItem/',deleteItem),
    url(r'finishedItem/',finishedItem),
    url(r'sendFrontItme/',sendFrontItme),
]
