from django.contrib import admin

# Register your models here.
print("rbac.............")

from .models import *


class UserInfoConfig(admin.ModelAdmin):
    list_display = ["id", "name", "email"]
    # list_display_links = ('name',"email")
    # ordering=["id",]
    # search_fields=["name","email"]
    # list_filter=["roles"]
    # list_editable=['name']
    # fields=["name"]
    # exclude=["name"]
    # readonly_fields=["name"]

    # fieldsets = (
    #     ('AAAA', {
    #         'fields': ('name', 'email')
    #     }),
    #
    #     ('其他', {
    #         'classes': ('collapse', 'wide', 'extrapretty'),  # 'collapse','wide', 'extrapretty'
    #         'fields': ('roles',),
    #     }),
    # )

    def foo(self, request, queryset):
        print(queryset)
        queryset.update(email="yuan@qq.com")

    foo.short_description = "中文显示自定义Actions"
    actions = [foo,]
admin.site.register(User,UserInfoConfig)


class RoleConfig(admin.ModelAdmin):
    list_display = ["id","title"]
admin.site.register(Role,RoleConfig)



class PermissionGroupConfig(admin.ModelAdmin):
    list_display = ["caption","menu"]
admin.site.register(PermissionGroup,PermissionGroupConfig)


class Menuconfig(admin.ModelAdmin):
    list_display = ["id","caption"]
admin.site.register(Menu,Menuconfig)



class PermissionConfig(admin.ModelAdmin):
    list_display = ["id","title","url","permission_group","code","parent"]
    ordering = ["id"]
admin.site.register(Permission,PermissionConfig)


print(admin.site._registry)

#  {Book:v1,UserInfo:v2,}