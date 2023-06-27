import traceback

from django.http import JsonResponse
from django.db.models import Q

from common.models import Device_items
from django.core.paginator import Paginator, EmptyPage

import json


def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数 在 request 对象的 GET属性中
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_device':
        return list_device(request)
    elif action == 'add_device':
        return add_device(request)
    elif action == 'del_device':
        return delete_device(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def list_device(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        # .order_by('-id') 表示按照 id字段的值 倒序排列
        # 这样可以保证最新的记录显示在最前面
        qs = Device_items.objects.values().order_by('-id')

        # 查看是否有 关键字 搜索 参数
        keywords = request.params.get('keywords', None)
        if keywords:
            conditions = [Q(device_id__contains=one) for one in keywords.split(' ') if one] # 查询设备id
            query = Q()
            for condition in conditions:
                query &= condition
            qs = qs.filter(query)
        # 要获取的第几页
        pagenum = request.params['pagenum']

        # 每页要显示多少条记录
        pagesize = request.params['pagesize']

        # 使用分页对象，设定每页多少条记录
        pgnt = Paginator(qs, pagesize)

        # 从数据库中读取数据，指定读取其中第几页
        page = pgnt.page(pagenum)

        # 将 QuerySet 对象 转化为 list 类型
        retlist = list(page)

        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist, 'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


def add_device(request):
    info = request.params['data']

    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    device = Device_items.objects.create(category=info['category'],
                                         device_id=info['device_id'],
                                         MAC=info['MAC'],
                                         IP=info['IP'],
                                         area=info['area'],
                                         netstatus=info['netstatus'],
                                         authentication=info['authentication'],
                                         longitude=info['longitude'],
                                         latitude=info['latitude'],
                                         battery=info['battery'],
                                           )

    return JsonResponse({'ret': 0, 'id': device.id})


def delete_device(request):
    device_id = request.params['device_id']

    try:
        # 根据 id 从数据库中找到相应的药品记录
        device = Device_items.objects.get(device_id=device_id)
    except Device_items.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{device_id}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    device.delete()

    return JsonResponse({'ret': 0})

