#!/usr/bin/env python
# coding=utf-8
from django.core.mail import send_mail

def sendEmail(email, code):
    title = "验证码"
    subTitle = u"您的验证码是："+ code
    result = send_mail(title, subTitle, '1304835707@qq.com', [email])
    return result
