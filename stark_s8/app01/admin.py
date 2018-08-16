from django.contrib import admin

# Register your models here.
from .models import *

from django.utils.safestring import mark_safe

class BookConfig(admin.ModelAdmin):

    def edit(self):
        return mark_safe("<a href=''>编辑</a>")

    def delete(self):
        return mark_safe("<a href=''>删除</a>")

    list_display = ["id", "title","price",edit,delete]

    list_filter = ["title","state","publish","authors"]

    #search_fields = ["title"]


admin.site.register(Book,BookConfig)
admin.site.register(author)
admin.site.register(Publish)
