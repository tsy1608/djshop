import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# 查询
from django.views.decorators.csrf import csrf_exempt

from cart.models import Cart


@csrf_exempt
def get(request):
    # 响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    try:
        # 请求对象
        userId = request.GET.get("user","")
        # 根据用户id查询该用户的所有购物车数据
        list = Cart.objects.filter(id_user_id=userId).all()
        # JSON格式化
        json_cart = json.loads(serializers.serialize('json', list, use_natural_foreign_keys=True))
        for i in range(len(list)):
            json_cart[i]['fields']['id'] = list[i].id
        response['data'] = json_cart
    except:
        response['data'] = ''
        response['code'] = 0
        response['msg'] = "失败",
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
    # 请求对象
    body = json.loads(request.body.decode("utf-8"))
    # 请求参数
    query = {}
    query['id'] = body['id']
    # 查询数据
    Cart.objects.filter(id=query['id']).delete()
    response['data'] = []
    # 响应结果对象
    return JsonResponse(response)


# @csrf_exempt表示视图可以进行跨域请求
@csrf_exempt
def add(request):
    # 响应对象
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
        query['id_user_id'] = body['user']
        query['id_goods_id'] = body['goods']
        query['id_sku_id'] = body['sku']
        query['count'] = body['count']
        # 根据用户id查询该用户的所有购物车数据
        list = Cart.objects.filter(id_user_id=query['id_user_id']).all()
        # 判断该商品是否已经添加过购物车
        exists = False
        # 循环对比，判断是否已经添加过
        for car in list:
            # 如果spuid相同，skuid页相同，则说明已经添加过
            if car.id_goods_id == query['id_goods_id'] and car.id_sku_id == query['id_sku_id']:
                car.count = int(query['count']) + car.count	# 商品数量累加
                car.save()	# 更新原数据，不新增
                exists = True	# 设置存在标记为True
                break
        # 如果存在标记为False，则新添加购物车
        if exists == False:
            # 创建对象
            cart = Cart(id_user_id=query['id_user_id'], id_goods_id=query['id_goods_id'], id_sku_id=query['id_sku_id'], count=query['count'])
            # 查询数据
            cart.save()
    except:
        response['data'] = ''
        response['code'] = 0
        response['msg'] = "失败",
    # 响应结果对象
    return JsonResponse(response)