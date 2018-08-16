from django.contrib import admin

# Register your models here.


from .models import *


class A(admin.ModelAdmin):
    list_display=["id","name","email"]

admin.site.register(UserInfo,A)




admin.site.register(Role)

class PermissionGroupConfig(admin.ModelAdmin):
    list_display = ["caption","menu"]
admin.site.register(PermissionGroup,PermissionGroupConfig)
admin.site.register(Menu)

class PermissionConfig(admin.ModelAdmin):
    list_display = ["id","title","url","permission_group","code","parent"]
    ordering = ["id"]
admin.site.register(Permission,PermissionConfig)




