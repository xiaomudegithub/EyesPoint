# **coding:utf8**
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
import time

from Login.views import *
from models import *

# Create your views here.

@api_view(['POST'])
def unfinishedItems(request):
    response = ResponseObject()    
    try:
        userId = request.data["userId"]
    except:
        response.errorCode = -201
        response.msg = "无用户信息"
        return HttpResponse(json.dumps(response.__dict__))
    try:
        items = ItemModel.objects.filter(userId=userId,isDelete=False,isFinished=False)
        itemArray = []
        for item in items:
            itemDic = model_to_dict(item)
            itemArray.append(itemDic)
        response.content = itemArray
        response.msg = "查询成功"
        response.errorCode = 200
        return HttpResponse(json.dumps(response.__dict__))
    except ItemModel.DoesNotExist:
        response.errorCode = -202
        response.msg = "数据为空"
        response.content = []
        return HttpResponse(json.dumps(response.__dict__))
    

@api_view(["POST"])
def historyItems(request):
    response = ResponseObject()    
    try:
        userId = request.data["userId"]
    except:
        response.errorCode = -201
        response.msg = "无用户信息"
        return HttpResponse(json.dumps(response.__dict__))
    try:
        items = ItemModel.objects.filter(userId=userId,isDelete=False,isFinished=True)
        itemArray = []
        for item in items:
            itemDic = model_to_dict(item)
            itemArray.append(itemDic)
        response.content = itemArray
        response.msg = "查询成功"
        response.errorCode = 200
        return HttpResponse(json.dumps(response.__dict__))
    except ItemModel.DoesNotExist:
        response.errorCode = -202
        response.msg = "数据为空"
        response.content = []
        return HttpResponse(json.dumps(response.__dict__))

@api_view(["POST"])
def addItem(request):
    response = ResponseObject()
    response.msg = "缺少参数："
    for key in ["title", "content", "rank", "userId"]:
        if key in request.data.keys():
            continue
        response.errorCode = -203
        response.msg += key+","
    if response.errorCode == -203:
        return HttpResponse(json.dumps(response.__dict__))

    try:
        item = ItemModel()
        item.title = request.data["title"]
        item.content = request.data["content"]
        item.rank = request.data["rank"]
        item.userId = request.data["userId"]
        item.save()
        response.errorCode = 200
        response.msg = "加入成功"
        response.success = True
        return HttpResponse(json.dumps(response.__dict__))
    except:
        response.errorCode = -204
        response.msg = "加入失败，请稍候再试"
        return HttpResponse(json.dumps(response.__dict__))

@api_view(["POST"])
def deleteItem(request):
    response = ResponseObject()
    response.msg = "缺少参数："
    for key in ["itemId", "userId"]:
        if key in request.data.keys():
            continue
        response.errorCode = -203
        response.msg += key+","
    if response.errorCode == -203:
        return HttpResponse(json.dumps(response.__dict__))
    try:
        item = ItemModel.objects.get(ok=request.data["itemId"])
        item.isDeleted = True
        item.save()
        response.errorCode = 200
        response.msg = "删除成功"
        response.success = True
        return HttpResponse(json.dumps(response.__dict__))
    except ItemModel.DoesNotExist:
        response.errorCode = -205
        response.msg = "查询不到该条目"
        return HttpResponse(json.dumps(response.__dict__))
    except:
        response.errorCode = -206
        response.msg = "删除失败，请稍后再试"
        return HttpResponse(json.dumps(response.__dict__))



@api_view(["POST"])
def finishedItem(request):
    response = ResponseObject()
    response.msg = "缺少参数："
    for key in ["itemId", "userId"]:
        if key in request.data.keys():
            continue
        response.errorCode = -203
        response.msg += key+","
    if response.errorCode == -203:
        return HttpResponse(json.dumps(response.__dict__))
    try:
        item = ItemModel.objects.get(ok=request.data["itemId"])
        item.isFinished = True
        item.save()
        response.errorCode = 200
        response.msg = "提交成功"
        response.success = True
        return HttpResponse(json.dumps(response.__dict__))
    except ItemModel.DoesNotExist:
        response.errorCode = -205
        response.msg = "查询不到该条目"
        return HttpResponse(json.dumps(response.__dict__))
    except:
        response.errorCode = -207
        response.msg = "完成提交失败，请稍后再试"
        return HttpResponse(json.dumps(response.__dict__))

@api_view(["POST"])
def sendFrontItme(request):
    response = ResponseObject()
    response.msg = "缺少参数："
    for key in ["itemId", "userId"]:
        if key in request.data.keys():
            continue
        response.errorCode = -203
        response.msg += key+","
    if response.errorCode == -203:
        return HttpResponse(json.dumps(response.__dict__))
    try:
        item = ItemModel.objects.get(ok=request.data["itemId"])
        item.rank = request.data["rank"]
        item.save()
        response.errorCode = 200
        response.msg = "删除成功"
        response.success = True
        return HttpResponse(json.dumps(response.__dict__))
    except ItemModel.DoesNotExist:
        response.errorCode = -205
        response.msg = "查询不到该条目"
        return HttpResponse(json.dumps(response.__dict__))
    except:
        response.errorCode = -207
        response.msg = "设置失败，请稍后再试"
        return HttpResponse(json.dumps(response.__dict__))
