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

class ResponseObject():
    def __init__(self):
        self.success = False
        self.errorCode = -1
        self.msg = ""
        self.content = None

# Create your views here.
def test(request):
    return HttpResponse("Hello world")

@api_view(['POST'])
def postTest(request):
    return HttpResponse(request.data["test"])


@api_view(['POST'])
def getValidCode(request):
    email = request.data["email"]
    response = ResponseObject()
    try:
        codeMode = ValidCode.objects.get(userEmail=email)
        if time.time() - float(codeMode.timestamp) < 10:
            response.errorCode = -101
            response.msg = "发送频繁,请稍候再试"
            return HttpResponse(json.dumps(response.__dict__))
        else:
            sendValidCode(email, codeMode)
            response.errorCode = 200
            response.msg = "验证码重新发送成功"
            response.success = True
            return HttpResponse(json.dumps(response.__dict__))
    except ValidCode.DoesNotExist:
        success = sendValidCode(email)
        if not success:
            response.errorCode = -102
            response.msg = "发送失败,请稍候再试"
            return HttpResponse(json.dumps(response.__dict__)) 
        response.errorCode = 200
        response.msg = "验证码发送成功"
        response.success = True
        return HttpResponse(json.dumps(response.__dict__))

@api_view(['POST'])
def checkValidCode(request):
    response = ResponseObject()
    try:
        email = request.data["email"]
    except:
        response.errorCode = -103
        response.msg = "请输入邮箱"
        return HttpResponse(json.dumps(response.__dict__)) 

    try:
        code = request.data["code"]
    except:
        response.errorCode = -104
        response.msg = "请输入验证码"
        return HttpResponse(json.dumps(response.__dict__)) 

    try:
        codeMode = ValidCode.objects.get(userEmail=email)
        if time.time() - float(codeMode.timestamp) > 60 * 5:
            response.errorCode = -105
            response.msg = "验证码已过期"
            return HttpResponse(json.dumps(response.__dict__)) 
        if codeMode.valCode == code:
            token = md5(email + code)
            codeMode.accesstoken = token
            codeMode.save()
            response.errorCode = 200
            response.msg = "短信验证码通过"
            response.success = True
            response.content = {"accesstoken":token}
            return HttpResponse(json.dumps(response.__dict__))
        else:
            response.errorCode = -106
            response.msg = "验证码错误"
            return HttpResponse(json.dumps(response.__dict__)) 
    except ValidCode.DoesNotExist:
        response.errorCode = -107
        response.msg = "邮箱未注册"
        return HttpResponse(json.dumps(response.__dict__)) 

@api_view(['POST'])
def registerOrUpdatepwd(request):
    response = ResponseObject()
    try:
        email = request.data["email"]
    except:
        response.errorCode = -103
        response.msg = "请输入邮箱"
        return HttpResponse(json.dumps(response.__dict__)) 

    try:
        pwd = request.data["passwd"]
    except:
        response.errorCode = -108
        response.msg = "请输入密码"
        return HttpResponse(json.dumps(response.__dict__)) 

    try:
        accesstoken = request.data["accesstoken"]
    except:
        response.errorCode = -109
        response.msg = "accesstoken不存在"
        return HttpResponse(json.dumps(response.__dict__)) 

    try:
        codeMode = ValidCode.objects.get(userEmail=email)
        if codeMode.accesstoken != accesstoken:
            response.errorCode = -111
            response.msg = "accesstoken不正确"
            return HttpResponse(json.dumps(response.__dict__)) 
    except ValidCode.DoesNotExist:
        response.errorCode = -110
        response.msg = "邮箱未注册"
        return HttpResponse(json.dumps(response.__dict__)) 
    
    response.errorCode = 200
    response.success = True
    
    try:
        user = User.objects.get(userEmail=email)
        user.pwd = pwd
        user.accesstoken = accesstoken
        user.save() 
        response.msg = "密码更新成功"
        return HttpResponse(json.dumps(response.__dict__)) 
    except User.DoesNotExist:
        user = User(userEmail = email, pwd = pwd, accesstoken = accesstoken)
        user.save()
        response.msg = "注册成功"
        return HttpResponse(json.dumps(response.__dict__)) 

@api_view(["POST"])
def login(request):
    response = ResponseObject()
    try:
        email = request.data["email"]
    except:
        response.errorCode = -103
        response.msg = "请输入邮箱"
        return HttpResponse(json.dumps(response.__dict__)) 

    try:
        pwd = request.data["passwd"]
    except:
        response.errorCode = -108
        response.msg = "请输入密码"
        return HttpResponse(json.dumps(response.__dict__)) 

    try:
        user = User.objects.get(userEmail=email)
        if user.pwd == pwd:
            response.errorCode = 200
            response.msg = "登录成功"
            response.success = True
            response.content = {"accesstoken":user.accesstoken}
            return HttpResponse(json.dumps(response.__dict__)) 
        else:
            response.errorCode = -113
            response.msg = "密码错误"
            return HttpResponse(json.dumps(response.__dict__)) 
    except User.DoesNotExist:
        response.errorCode = -112
        response.msg = "用户未注册"
        return HttpResponse(json.dumps(response.__dict__)) 



def sendValidCode(email, model=None):
    code = str(random.randint(100000,999999))
    if sendEmail(email, code):
        if model:
            model.valCode = code
            model.timestamp = str(time.time())
            model.save()
            return True
        code = ValidCode(userEmail=email, valCode=code, timestamp=str(time.time()), accesstoken=None)
        code.save()
        return True
    else:
        return False
