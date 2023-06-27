import requests, pprint

# 发送列出请求，注意多了 pagenum 和 pagesize
# 测试list_device

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接

payload = {
    'action': 'list_extremeweather',
    'pagenum': 1,
    'pagesize': 5,
    # 'keywords': 1
}

response = requests.get('http://8.146.201.158:8000/api/user/information',
                        params=payload,
                        )
pprint.pprint(response.json())