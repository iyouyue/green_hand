

from django.conf.urls import url,include
from django.contrib import admin

from blog import views



urlpatterns = [
    # 文章详细页的点赞URL
    url(r'^digg/$', views.digg),
    url(r'^comment/$', views.comment),
    url(r'^get_comment_tree/(\d+)/$', views.get_comment_tree),

    url(r'^(?P<username>\w+)/backend/$', views.backend),
    url(r'^(?P<username>\w+)/backend_add_article/$', views.backend_add_article),

    # 个人站点的url配置
    url(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)\.html/$', views.article_detail),
    url(r'^(?P<username>\w+)/$', views.home_site), # home_site(request,username="wupeiqi")
    url(r'^(?P<username>\w+)/(?P<condition>cate|tag|date)/(?P<params>(\w+/?\w+))$', views.home_site), # home_site(username="wupeiqi")

]