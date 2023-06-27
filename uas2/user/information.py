import traceback
from django.http import JsonResponse

# 导入 Medicine 对象定义
# from common.models import Earthquake
from django.core.paginator import Paginator, EmptyPage
import json
from extreme_data import main_code_ext
from earthquake_data import main_code_ear


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
    if action == 'list_earthquake':
        return list_earthquake(request)
    elif action == 'list_extremeweather':
        return list_extremeweather(request)
    elif action == 'list_province':
        return list_province(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def list_earthquake(request):
    try:
        # 要获取的第几页
        pagenum = request.params['pagenum']

        # 每页要显示多少条记录
        pagesize = request.params['pagesize']

        pagenum = int(pagenum)
        pagesize = int(pagesize)
        # 使用函数读取所有最近的数据
        all_data = json.loads(main_code_ear.craw_earthquake())
        # 选取符合要求的页
        try:
            data = all_data[pagesize*(pagenum-1):pagesize*pagenum]
        except:
            data = all_data[pagesize * (pagenum - 1):]

        return JsonResponse({'ret': 0, 'retlist': data, 'total': len(all_data)})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


def list_extremeweather(request):
    try:
        # 要获取的第几页
        pagenum = request.params['pagenum']

        # 每页要显示多少条记录
        pagesize = request.params['pagesize']
        pagenum = int(pagenum)
        pagesize = int(pagesize)
        # 使用函数读取所有最近的数据
        all_data = json.loads(main_code_ext.craw_extremeweather())
        # 选取符合要求的页
        try:
            data = all_data[pagesize * (pagenum - 1):pagesize * pagenum]
        except:
            data = all_data[pagesize * (pagenum - 1):]

        return JsonResponse({'ret': 0, 'retlist': data, 'total': len(all_data)})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


def list_province(request):
    try:

        # 使用函数读取所有最近的数据
        all_data_ear = json.loads(main_code_ear.craw_earthquake())
        all_data_ext = json.loads(main_code_ext.craw_extremeweather())
        # 读取省份
        province = request.params.get('keywords', None)
        earthquake_list = []
        weather_list = []
        for info in all_data_ear:
            if info['province'] == province:
                earthquake_list.append(info)
        for info in all_data_ext:
            if info['province'] == province:
                weather_list.append(info)

        return JsonResponse({'ret': 0, 'earthquake_list': earthquake_list, 'weather_list': weather_list})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})







