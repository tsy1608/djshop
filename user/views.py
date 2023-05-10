import json
import random

from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# 用户登录
from django.views.decorators.csrf import csrf_exempt
from user.models import User

@csrf_exempt
def signin(request):
    # 响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    # 请求对象
    body = json.loads(request.body.decode("utf-8"))
    # 查询数据
    list = User.objects.filter(username=body['username'],is_delete=False)
    if check_password(body['password'],list[0].password):
        # JSON格式化
        json_user = json.loads(serializers.serialize('json', list, use_natural_foreign_keys=True))
        json_user[0]['fields']['id'] = list[0].id
        json_user[0]['fields']['avatar'] = 'http://127.0.0.1:8000/' + json_user[0]['fields']['avatar']
        response['data'] = json_user
    else:
        response['data'] = []
    # 响应结果对象
    return JsonResponse(response)


@csrf_exempt
def signup(request):
    # 响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    # 请求对象
    body = json.loads(request.body.decode("utf-8"))

    # 字符串类型的加密盐值
    salt = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
    # 查询数据
    # password = make_password(body['password'], salt)
    user = User(username=body['username'], password=body['password'], salt=salt)
    user.save()
    list = User.objects.filter(id=user.id)
    # JSON格式化
    json_user = json.loads(serializers.serialize('json', list))
    json_user[0]['fields']['id'] = user.id
    response['data'] = json_user
    # 响应结果对象
    return JsonResponse(response)


@csrf_exempt
def delete(request):
    # 响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    try:
        # 请求对象
        body = json.loads(request.body.decode("utf-8"))
        # 查询数据
        users = User.objects.filter(id=body['id']).first()
        users.is_delete = True
        users.save()
    except:
        response['data'] = ''
        response['code'] = 0
        response['msg'] = "失败",
    # 响应结果对象
    return JsonResponse(response)


@csrf_exempt
def remove(request):
    # 响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    try:
        # 请求对象
        body = json.loads(request.body.decode("utf-8"))
        # 查询数据
        User.objects.filter(id=body['id']).first().delete()
    except:
        response['data'] = ''
        response['code'] = 0
        response['msg'] = "失败",
    # 响应结果对象
    return JsonResponse(response)