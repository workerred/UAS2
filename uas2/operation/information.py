import traceback
from django.http import JsonResponse

# 导入 Medicine 对象定义
# from common.models import Earthquake
from django.core.paginator import Paginator, EmptyPage
import json
from shanxi_weather import craw_shanxi


def dispatcher(request):

    # GET请求 参数 在 request 对象的 GET属性中
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_shanxi_disaster':
        return list_shanxi_disaster(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def list_shanxi_disaster(request):
    try:

        # 使用函数读取所有最近的数据
        all_data_shanxi = json.loads(craw_shanxi.craw_shanxi_weather())
        # 读取省份
        city = request.params.get('keywords', None)
        retlist = []
        for info in all_data_shanxi:
            if info['city'] == city:
                retlist.append(info)
                break

        return JsonResponse({'ret': 0, 'retlist': retlist})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})