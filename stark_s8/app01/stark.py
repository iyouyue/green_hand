
from stark.service.sites import site,ModelSatrk

from .models import *

from django.utils.safestring import mark_safe


from django.urls import reverse


from django.forms import ModelForm
class BookModelForm(ModelForm):
    class Meta:
        model=Book
        fields="__all__"
        error_messages={
            "title":{"required":"不能为空"},
            "price":{"required":"不能为空"},
        }


class BookConfig(ModelSatrk):

    def state(self,obj=None,is_header=False):
        if is_header:
            return "状态"
        return obj.get_state_display()

    list_display = [state,"title","publish","authors"]
    model_form_class = BookModelForm
    list_display_links = ["title"]
    search_fields = ["title","price"]

    def patch_init(self,queryset):
        queryset.update(price=100)

        return "初始化成功"

    patch_init.desc="批量初始化"
    actions = [patch_init,]

    list_filter = ["title","state","publish","authors"]


site.register(Book,BookConfig)

site.register(author)
site.register(Publish)








