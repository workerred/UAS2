import traceback

from django.http import JsonResponse
from django.db.models import Q

from common.models import Task
from django.core.paginator import Paginator, EmptyPage

import json
import datetime


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
    if action == 'list_task_abstract':
        return list_task_abstract(request)
    elif action == 'list_task_detail':
        return list_task_detail(request)
    elif action == 'add_task':
        return add_task(request)
    elif action == 'del_task':
        return del_task(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def list_task_abstract(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        # .order_by('-id') 表示按照 id字段的值 倒序排列
        # 这样可以保证最新的记录显示在最前面
        qs = Task.objects.values().order_by('-id')

        # 查看是否有 关键字 搜索 参数
        keywords = request.params.get('keywords', None)
        monthfilter = request.params.get('month', None)
        # 年月筛选
        if monthfilter:
            conditions = [Q(creationmonth__contains=one) for one in monthfilter.split(' ') if one]  # 查询任务名
            query = Q()
            for condition in conditions:
                query &= condition
            qs = qs.filter(query)
        # id查询
        if keywords:
            conditions = [Q(id__contains=one) for one in keywords.split(' ') if one]  # 查询任务名
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

        # 删除多余的label
        for dic in page:
            del dic['tasktype']
            del dic['creationmonth']
        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist, 'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


def list_task_detail(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        # .order_by('-id') 表示按照 id字段的值 倒序排列
        # 这样可以保证最新的记录显示在最前面
        qs = Task.objects.values().order_by('-id')

        # 查看是否有 关键字 搜索 参数
        keywords = request.params.get('keywords', None)
        monthfilter = request.params.get('month', None)
        # 年月筛选
        if monthfilter:
            conditions = [Q(creationmonth__contains=one) for one in monthfilter.split(' ') if one]  # 查询任务名
            query = Q()
            for condition in conditions:
                query &= condition
            qs = qs.filter(query)
        # id查询
        if keywords:
            conditions = [Q(id__contains=one) for one in keywords.split(' ') if one]  # 查询任务id
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

        #删除多余的label
        for dic in page:
            del dic['creationmonth']
        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist, 'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


def add_task(request):
    info = request.params['data']
    # 获取当前时间
    now_time = datetime.datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
    now_month = datetime.datetime.now().strftime('%Y-%m') # 添加年月标签
    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    task = Task.objects.create(taskname=info['taskname'],
                               tasktype=info['tasktype'],
                               longitude=info['longitude'],
                               latitude=info['latitude'],
                               radius=info['radius'],
                               distribution=info['distribution'],
                               creationtime=now_time,
                               creationmonth=now_month
                               )

    return JsonResponse({'ret': 0, 'id': task.id})


def del_task(request):
    task_id = request.params['task_id']

    try:
        # 根据 id 从数据库中找到相应的任务记录
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{task_id}`的任务不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    task.delete()

    return JsonResponse({'ret': 0})
