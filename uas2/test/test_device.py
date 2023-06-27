import requests, pprint

# 发送列出请求，注意多了 pagenum 和 pagesize
# 测试list_device

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接

payload = {
    'action': 'list_device',
    'pagenum': 1,
    'pagesize': 2,
    # 'keywords': 1
}

response = requests.get('http://8.146.201.158:8000/api/operation/device',
                        params=payload,
                        )
pprint.pprint(response.json())

# 测试add_device
# data = {
#     'action': 'add_device',
#     'data': {
#         'IP': '2131564',
#         'MAC': '121313',
#         'area': '陕西西安',
#         'authentication': '已认证',
#         'battery': '99%',
#         'category': '种类2',
#         'device_id': 2,
#         'latitude': '30.00',
#         'longitude': '110.00',
#         'netstatus': '成功'
#     }
# }
#
# response = requests.post('http://8.146.201.158:8000/api/operation/device',
#                          json=data,
#                          )
# print(response)
# pprint.pprint(response.json())
