from django.urls import path

from user import information

urlpatterns = [

    path('information', information.dispatcher),

]