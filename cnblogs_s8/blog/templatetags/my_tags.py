from django import template
from django.utils.safestring import mark_safe
from blog.models import *

from django.db.models import Count
register = template.Library()  # register的名字是固定的,不可改变

@register.inclusion_tag("blog/archive.html")
def get_archive_style(username):
        user = UserInfo.objects.filter(username=username).first()
        # 当前站点
        blog = user.blog
        # 查询当前站点的所有分类
        # category_list=Category.objects.filter(blog=blog)
        # category_list=Category.objects.filter(blog_id=blog.pk)

        # 查询每一个分类名称以及对应的文章数
        # Category.objects.all().annotate(c=Count("article")).values_list("title","c")
        cate_list = Category.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
        # print(ret)
        # 查询但当前站点每一个标签名称以及对应的文章数
        tag_list = Tag.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
        print(tag_list)
        # 日期归档   [["2018-02",5],["2010-9",6]]
        date_ist = Article.objects.filter(user=user) \
            .extra(select={"create_time_ym": "strftime('%%Y/%%m',create_time)"}) \
            .values("create_time_ym") \
            .annotate(c=Count("nid")).values_list("create_time_ym", "c")

        return {"cate_list":cate_list,"tag_list":tag_list,"date_ist":date_ist,"username":username}






@register.filter
def filter_multi(v1,v2):
    return  v1 * v2

@register.simple_tag
def simple_tag_multi(v1,v2):
    return  v1 * v2