import json
import uuid

from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from cart.models import Cart
from goods.models import Goods, Sku
from order.models import Order, OrderItem


@csrf_exempt
def list(request):
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
        query['page'] = body['page']
        query['limit'] = body['limit']
        query['key'] = body['key']
        # 查询数据:模糊查询
        list_order = Order.objects.all()
        for i in range(len(list_order)):
            list_order[i].order_status = list_order[i].get_order_status_display()
        # JSON格式化
        paginator = Paginator(list_order, query['limit'])
        response['total'] = paginator.count
        records = paginator.page(query['page'])
        json_order = json.loads(serializers.serialize('json', records, use_natural_foreign_keys=True))
        for i in range(len(records)):
            json_order[i]['order_status'] = records[i].get_order_status_display()
            list_order_item = OrderItem.objects.filter(id_order=records[i].sn).all()
            json_order[i]['fields']['item'] = json.loads(serializers.serialize('json', list_order_item))
        response['data'] = json_order
    except:
        response['data'] = ''
        response['code'] = 0
        response['msg'] = "失败",
    # 响应结果对象
    return JsonResponse(response)


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
        # 订单号
        sn = uuid.uuid1().hex

        goods_total_count = 0
        goods_total_amount = 0
        goods_pay_amount = 0
        items = body['item']
        for item in items:
            # 查询goods，获取商品名称和图片
            o_goods = Goods.objects.filter(id=item['goods']).first()

            # 根据skuid和spuid查询sku，获取商品价格
            o_sku = Sku.objects.filter(id=item['sku'], id_goods_id=item['goods']).first()

            # 计算总金额，减去折扣和优惠，得到支付总金额
            total_amount = o_sku.price * int(item['count'])
            pay_amount = total_amount

            # 保存订单商品
            orderitem = OrderItem(id_goods_id=o_goods.id, id_sku_id=o_sku.id, id_order=sn, count=item['count'],
                                  name=o_goods.name, total_amount=total_amount, pay_amount=pay_amount,
                                  price=o_sku.price, pic=item['pic'])
            orderitem.save()

            # 减库存
            o_sku.stock = o_sku.stock - int(item['count'])
            o_sku.save()

            # 清购物车
            Cart.objects.filter(id=item['id']).delete()

            # 计算订单数据
            goods_total_count = goods_total_count + item['count']
            goods_total_amount = goods_total_amount + total_amount
            goods_pay_amount = goods_pay_amount + pay_amount

        # 创建订单
        order = Order(sn=sn, id_user_id=body['user'], total_count=body['total_count'],
                      total_amount=body['total_amount'],
                      postage=body['postage'])
        # 查询数据
        order.save()
        response['data'] = {"id": order.id, "sn": sn}
    except:
        response['data'] = ''
        response['code'] = 0
        response['msg'] = "失败",
    # 响应结果对象
    return JsonResponse(response)


@csrf_exempt
def pay(request):
    # 响应对象
    response = {
        'code': 20000,
        'success': True,
        'msg': "成功",
    }
    try:
        # 请求对象
        body = json.loads(request.body.decode("utf-8"))
        # 前端发起微信或者支付宝支付
        # 判断支付成功
        # 支付成功后将[流水号、支付方式、实付金额、支付时间]等存入订单表中
        order = Order.objects.filter(id=body['id']).first()
        order.pay_code = uuid.uuid1().hex
        order.pay_type = 1 #'支付宝'
        order.pay_amount = order.total_amount
        order.pay_time = timezone.now()
        # 修改订单状态为已支付
        order.order_status = 2 # 已支付
        # 查询数据
        order.save()
        response['data'] = {"status": 2}
    except:
        response['data'] = ''
        response['code'] = 0
        response['msg'] = "失败",
    # 响应结果对象
    return JsonResponse(response)
