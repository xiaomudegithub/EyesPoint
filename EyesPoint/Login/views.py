#*coding:utf8*
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
import time
import random

from models import *
from  email import *
from md5 import *

# Create your views here.
def test(request):
    return HttpResponse("Hello world")

@api_view(['POST'])
def postTest(request):
    return HttpResponse(request.data["test"])


@api_view(['POST'])
def getValidCode(request):
    email = request.data["email"]
    try:
        codeMode = ValidCode.objects.get(userEmail=email)
        if time.time() - float(codeMode.timestamp) < 10:
            return HttpResponse(json.dumps({"success":False,"msg":"发送频繁,请稍候再试"}))
        else:
            sendValidCode(email, codeMode)
            return HttpResponse(json.dumps({"success":True,"msg":"重新发送成功"}))
    except ValidCode.DoesNotExist:
        success = sendValidCode(email)
        return HttpResponse(json.dumps({"success":True,"msg":"发送成功"}))

@api_view(['POST'])
def checkValidCode(request):
    try:
        email = request.data["email"]
    except:
        return HttpResponse(json.dumps({"success":False,"msg":"请输入邮箱"}))

    try:
        code = request.data["code"]
    except:
        return HttpResponse(json.dumps({"success":False,"msg":"请输入验证码"}))

    try:
        codeMode = ValidCode.objects.get(userEmail=email)
        if time.time() - float(codeMode.timestamp) > 60 * 5:
            return HttpResponse(json.dumps({"success":False,"msg":"验证码已过期"}))
        if codeMode.valCode == code:
            token = md5(email + code)
            codeMode.accesstoken = token
            codeMode.save()
            return HttpResponse(json.dumps({"success":True, "accesstoken":token}))
        else:
            return HttpResponse(json.dumps({"success":False,"msg":"验证码错误"}))
    except ValidCode.DoesNotExist:
        return HttpResponse(json.dumps({"success":False,"msg":"邮箱未注册"}))

@api_view(['POST'])
def registerOrUpdatepwd(request):
    try:
        email = request.data["email"]
    except:
        return HttpResponse(json.dumps({"success":False,"msg":"请输入邮箱"}))

    try:
        pwd = request.data["passwd"]
    except:
        return HttpResponse(json.dumps({"success":False,"msg":"请输入密码"}))

    try:
        accesstoken = request.data["accesstoken"]
    except:
        return HttpResponse(json.dumps({"success":False,"msg":"accesstoken不存在"}))

    try:
        codeMode = ValidCode.objects.get(userEmail=email)
        if codeMode.accesstoken != accesstoken:
            return HttpResponse(json.dumps({"success":False,"msg":"accesstoken不正确"}))
    except ValidCode.DoesNotExist:
        return HttpResponse(json.dumps({"success":False,"msg":"邮箱未注册"}))
    
    try:
        user = User.objects.get(userEmail=email)
        user.pwd = pwd
        user.accesstoken = accesstoken
        user.save() 
        return HttpResponse(json.dumps({"success":True,"msg":"密码更新成功"}))
    except User.DoesNotExist:
        user = User(userEmail = email, pwd = pwd, accesstoken = accesstoken)
        user.save()
        return HttpResponse(json.dumps({"success":True,"msg":"注册成功"}))

@api_view(["POST"])
def login(request):
    try:
        email = request.data["email"]
    except:
        return HttpResponse(json.dumps({"success":False,"msg":"请输入邮箱"}))

    try:
        pwd = request.data["passwd"]
    except:
        return HttpResponse(json.dumps({"success":False,"msg":"请输入密码"}))

    try:
        user = User.objects.get(userEmail=email)
        if user.pwd == pwd:
            return HttpResponse(json.dumps({"success":True,"msg":"密码更新成功"}))
        else:
            return HttpResponse(json.dumps({"success":False, "msg":"密码错误"}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({"success":False, "msg":"用户未注册"}))



def sendValidCode(email, model=None):
    code = str(random.randint(100000,999999))
    if sendEmail(email, code):
        if model:
            model.valCode = code
            model.timestamp = str(time.time())
            model.save()
            return True
        code = ValidCode(userEmail=email, valCode=code, timestamp=str(time.time()))
        code.save()
        return True
    else:
        return False
