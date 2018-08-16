from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(UserInfo)

class RoleConfig(admin.ModelAdmin):
    change_list_template="change_list.html"
    list_display = ["id","title"]
admin.site.register(Role,RoleConfig)