

from django import template
from django.urls import reverse

register=template.Library()

from django.forms.models import ModelChoiceField


@register.inclusion_tag("stark/form.html")
def get_form(form,config):
    for bound_field in form:  # form组件下的每一个字段信息对象：bound_field
        # print("field",type(bound_field))
        # print(bound_field.name,bound_field.field)
        if isinstance(bound_field.field, ModelChoiceField):
            bound_field.is_pop = True
            # print(bound_field.field, type(bound_field.field))
            print(bound_field.field.queryset.model)

            app_label = bound_field.field.queryset.model._meta.app_label
            model_name = bound_field.field.queryset.model._meta.model_name
            _url = "%s_%s_add" % (app_label, model_name)

            print("model-name",config.model._meta.model_name)
            current_model_name=config.model._meta.model_name
            related_name=config.model._meta.get_field(bound_field.name).rel.related_name

            bound_field.url = reverse(_url) + "?pop_id=id_%s&current_model_name=%s&related_name=%s" % (bound_field.name,current_model_name,related_name)

    return {"form":form}



