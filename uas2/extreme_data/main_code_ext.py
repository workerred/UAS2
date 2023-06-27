import requests
import json
import pandas as pd
import json

def craw_category(num, province_list, city_list):

    # print(num)
    data = []  # 记录数据
    last_info = {}
    for i in range(7):  # 爬到第几页
        url = "https://www.qweather.com/v2/alarm/" + str(i+1) + "/" + str(num) + "/all.html"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }

        resp = requests.get(url, headers=headers)
        # print(resp.status_code)
        # print(resp.text)

        raw = json.loads(resp.text)  # 将解析网页的字符串内容转换为json格式
        # 逐一读取信息
        content = raw.get("data")  # 所有数据
        if len(content) == 0:
            break
        elif content[0] == last_info:
            break
        last_info = content[0]
        for info in content:
            level = info.get("level")
            title = info.get("title")
            # 匹配省份信息
            index = title.find("气")
            city = title[:index]
            flag = 0 # 是否匹配成功
            province = "0"
            for j in range(34):
                if city in city_list[j][0]:
                    province = province_list[j]
                    flag = 1 #匹配成功
                    break
            if flag == 0:
                continue
            time = info.get("time")
            data.append([level, title, time, province])
        # print("已读取页", i+1)
    return data


def craw_extremeweather():
    # 主函数
    data = []
    data_title = [["level", "title", "time", "province"]]
    # 省份列表
    province_list = ["陕西省", "北京市", "天津市", "上海市", "重庆市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", "湖北省", "湖南省", "广东省", "广西壮族自治区", "海南省", "四川省", "贵州省", "云南省", "西藏自治区","甘肃省","青海省","宁夏回族自治区","新疆维吾尔自治区","台湾省", "香港特别行政区", "澳门特别行政区"]
    # 城市列表
    city_list = []
    with open('C:\\Users\\Administrator\\Desktop\\uas2\\extreme_data\\城市列表.txt', 'r', encoding='utf-8') as f:# '城市列表.txt' C:\\Users\\Administrator\\Desktop\\uas2\\extreme_data\\城市列表.txt
        city_list.extend(x.strip().split(',') for x in f)
    for num in range(1001, 1058): # 1058
        newdata = craw_category(num, province_list, city_list)
        if len(newdata) != 0:
            data.extend(newdata)
    data = sorted(data, key=lambda x:x[2], reverse=True)
    data_title.extend(data)
    data = data_title # 对时间排序
    # 去重
    # 转换为json
    keys = data[0]
    list_json = [dict(zip(keys, item)) for item in data[1:]]
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)

    # df = pd.DataFrame(data[1:], columns=[data[0][0], data[0][1], data[0][2],data[0][3]])
    # df.to_excel("读取最近极端天气信息.xlsx", index=False)

    return str_json

