from django.urls import path

from operation import device, task, information

urlpatterns = [

    path('device', device.dispatcher),
    path('task', task.dispatcher),
    path('information', information.dispatcher)
]