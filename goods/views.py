import json

from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# @csrf_exempt表示视图可以进行跨域请求
from django.views.decorators.csrf import csrf_exempt

from goods.models import Goods, Sku


@csrf_exempt
def search(request):
    # 统一响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    try:
        # 请求对象
        body = json.loads(request.body.decode("utf-8"))
        # 请求参数
        query = {}
        query['page'] = body['page']
        query['limit'] = body['limit']
        query['key'] = body['key']
        # 查询数据:模糊查询
        list = Goods.objects.filter(name__contains=query['key']).all()
        # 分页插件
        paginator = Paginator(list, query['limit'])
        # 获取总条数
        response['total'] = paginator.count
        # 获取当前页数据集合
        records = paginator.page(query['page'])
        # 将数据序列号为JSON对象，并且关联查询外键的数据
        response['data'] = json.loads(serializers.serialize('json', records, use_natural_foreign_keys=True))
    except:
        response['data'] = ''
        response['code'] = 0
        response['msg'] = "失败",
    # 响应结果对象
    return JsonResponse(response)


# 广告
@csrf_exempt
def index(request):
    # 响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    # 查询数据
    list = Goods.objects.filter(is_new=True).all()
    # JSON格式化
    response['data'] = json.loads(serializers.serialize('json', list, use_natural_foreign_keys=True))
    # 响应结果对象
    return JsonResponse(response)


# 热推
@csrf_exempt
def hot(request):
    # 响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    # 查询数据
    list = Goods.objects.filter(is_hot=True).all()
    # JSON格式化
    response['data'] = json.loads(serializers.serialize('json', list, use_natural_foreign_keys=True))
    # 响应结果对象
    return JsonResponse(response)


# 详情
@csrf_exempt
def detail(request):
    # 响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    # 请求对象
    body = json.loads(request.body.decode("utf-8"))
    # 请求参数
    query = {}
    query['id'] = body['id']
    # 查询数据
    list_goods = Goods.objects.filter(**query).all()
    json_goods = json.loads(serializers.serialize('json', list_goods,use_natural_foreign_keys=True))
    for i in range(len(list_goods)):
        list_sku = Sku.objects.filter(id_goods_id=list_goods[i].id).all()
        json_sku = json.loads(serializers.serialize('json', list_sku, fields=['market_price', 'price', 'stock','attribute'], ))
        json_goods[i]['fields']['sku'] = json_sku
        json_goods[i]['fields']['skuid'] = 0
        json_goods[i]['fields']['id'] = list_goods[i].id
        for j in range(len(list_sku)):
            json_sku[j]['fields']['id'] = list_sku[j].id

    response['data'] = json_goods
    # response['sku'] = sku
    # 响应结果对象
    return JsonResponse(response)