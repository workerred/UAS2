from django.db import models


class Earthquake(models.Model):
    # 震级,小数位数为1
    level = models.DecimalField(decimal_places=1, max_digits=5)
    # 发震时间
    time = models.CharField(max_length=50)
    # 经度
    longitude = models.DecimalField(decimal_places=2, max_digits=10)
    # 纬度
    latitude = models.DecimalField(decimal_places=2, max_digits=10)
    # 深度
    depth = models.PositiveIntegerField()
    # 参考位置
    location = models.CharField(max_length=100)
    # 省
    province = models.CharField(max_length=10, null=True, blank=True)


class Extremeweather(models.Model):
    # 等级
    level = models.CharField(max_length=20)
    # 标题
    title = models.CharField(max_length=50)
    # 时间
    time = models.CharField(max_length=50)
    # 省
    province = models.CharField(max_length=10)


class Device_items(models.Model):
    # 设备类别
    category = models.CharField(max_length=20)
    # ID
    device_id = models.PositiveIntegerField(null=True, blank=True)
    # MAC
    MAC = models.CharField(max_length=20)
    # IP
    IP = models.CharField(max_length=20)
    # 地区
    area = models.CharField(max_length=20)
    # 组网状态
    netstatus = models.CharField(max_length=10)
    # 认证
    authentication = models.CharField(max_length=10)
    # 区域划分图的经度
    longitude = models.DecimalField(decimal_places=2, max_digits=5)
    # 区域划分图的纬度
    latitude = models.DecimalField(decimal_places=2, max_digits=5)
    # 电量
    battery = models.CharField(max_length=10)


class Task(models.Model):
    # 任务名
    taskname = models.CharField(max_length=20)
    # 任务类型
    tasktype = models.CharField(max_length=20)
    # 区域划分图的经度
    longitude = models.DecimalField(decimal_places=2, max_digits=5)
    # 区域划分图的纬度
    latitude = models.DecimalField(decimal_places=2, max_digits=5)
    # 半径
    radius = models.DecimalField(decimal_places=2, max_digits=10)
    # 无人机分配情况
    distribution = models.CharField(max_length=50)
    # 创建时间
    creationtime = models.CharField(max_length=30, null=True, blank=True)
    # 创建年月
    creationmonth = models.CharField(max_length=30, null=True, blank=True)