import requests
from bs4 import BeautifulSoup
import json


def craw_shanxi_weather():
    url = "https://m.baidu.com/sf"
    headers = {
        "User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"""
    }  # 使用三个引号防止里面有双引号

    params = {
        "pd": "life_compare_weather",
        "openapi": 1,
        "dspName": "iphone",
        "from_sf": 1,
        "resource_id": 4495,
        "word": "陕西天气",
        "title": "省市天气查询",
        "srcid": 4983,
        "fromSite": "pc"
    }
    resp = requests.get(url, headers=headers, params=params)
    # print(resp.status_code)
    # print(resp.text)

    # 读取网页
    soup = BeautifulSoup(resp.text, "html.parser")
    contents = soup.find("div", class_="sfc-wet-pro-weather-con c-gap-top")
    rows = contents.find_all("a")
    data = [["city", "temperature", "weather", "wind"]]
    # 天气对应列表
    wtr_indexout = ["晴", "阴", "雾", "小雨", "中雨", "大雨", "暴雨", "雷阵雨", "冰雹", "冻雨", "雨夹雪", "小雪", "中雪", "大雪", "霜冻", "大风", "多云"]
    wtr_indexin = ["qing", "yin", "wu", "xiaoyu", "zhongyu", "dayu", "baoyu", "leizhenyu", "bingbao", "dongyu",
                   "yujiaxue", "xiaoxue", "zhongxue", "daxue", "shuangdong", "dafeng", "duoyun"]
    for row in rows:
        city = row.find_all("div", class_="c-span3")[0].get_text()
        temp = row.find_all("div", class_="c-span3")[1].get_text()
        # 读天气
        wtr_list = row.find("div", class_="c-span2 c-gap-left sfc-wet-pro-weather-icon-po").find("div").find_all("div",
                                                                                                                 class_="c-span5")
        weather_list = []
        for wtr in wtr_list:
            weather = wtr.find("svg").find("use")["xlink:href"]
            weather_list.append(weather)
        # 转换中文天气
        weather = ''
        if len(weather_list) == 1:  # 只有一个天气的情况
            for i in range(len(wtr_indexin)):
                if wtr_indexin[i] in weather_list[0]:
                    weather = wtr_indexout[i]
        if len(weather_list) == 2:
            for i in range(2):
                for j in range(len(wtr_indexin)):
                    if wtr_indexin[j] in weather_list[i]:
                        weather += wtr_indexout[j]
                        if i == 0:
                            weather += '转'
                        break
        wind = row.find("div", class_="c-span4 sfc-wet-pro-weather-wind").get_text()

        data.append([city, temp, weather, wind])
    # 转换为json
    keys = data[0]
    list_json = [dict(zip(keys, item)) for item in data[1:]]
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)
    return str_json
