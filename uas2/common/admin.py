from django.contrib import admin

from .models import Earthquake, Extremeweather, Device_items

admin.site.register(Earthquake)
admin.site.register(Extremeweather)
admin.site.register(Device_items)
# Register your models here.
