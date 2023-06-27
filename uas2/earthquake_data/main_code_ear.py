import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json


def craw_earthquake():
    # 获取当前时间
    # now_time = datetime.datetime.now().strftime('%Y_%m_%d+%H_%M_%S')

    url = "https://news.ceic.ac.cn/index.html"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    # params = {
    #     "time": "1684050394"
    # } # 网址加上时间编码
    resp = requests.get(url, headers=headers)
    resp.encoding = "br"  # 网站是br编码
    # print(resp.status_code)
    # print(resp.text)
    # 份列表
    province_list = ["陕西", "北京", "天津", "上海", "重庆", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西",
                     "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "四川", "贵州", "云南", "西藏", "甘肃", "青海", "宁夏", "新疆", "台湾",
                     "香港", "澳门"]
    province_list2 = ["陕西省", "北京市", "天津市", "上海市", "重庆市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省", "江苏省", "浙江省",
                      "安徽省", "福建省", "江西省", "山东省", "河南省", "湖北省", "湖南省", "广东省", "广西壮族自治区", "海南省", "四川省", "贵州省", "云南省",
                      "西藏自治区", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区", "台湾省", "香港特别行政区", "澳门特别行政区"]

    # 解析网页
    soup = BeautifulSoup(resp.text, "html.parser")
    rows = soup.find_all("tr")  # 数据行
    idx = 0
    data = []
    for row in rows:
        onedata = []
        flag = 0  # 是否属于中国
        if idx == 0:  # 第一行为标题行
            # for th in row.find_all("th"):
            #     onedata.append(th.get_text())
            onedata.extend(['level', 'time', 'latitude', 'longitude', 'depth', 'location', 'province'])
            # print(onedata)
            data.append(onedata)
        else:  # 其他数据行
            for td in row.find_all("td"):
                onedata.append(td.get_text())
                for index in range(len(province_list)):
                    if province_list[index] in onedata[-1]:
                        onedata.append(province_list2[index])
                        flag = 1  # 属于中国
            if flag == 0:
                continue
            # print(onedata)
            data.append(onedata)
        idx += 1
    # 转换为json
    keys = data[0]
    list_json = [dict(zip(keys, item)) for item in data[1:]]
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)


    # 写入excel
    # df = pd.DataFrame(data[1:], columns=[data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6]])
    # df.to_excel("读取最近地震信息.xlsx", index = False)

    return str_json


#print(json.loads(craw_earthquake()))
