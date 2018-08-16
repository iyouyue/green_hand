"""s8_cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from blog import views
from django.views.static import serve
from s8_cnblog import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.log_in),
    url(r'^get_valid_img/', views.get_valid_img),
    url(r'^index/', views.index),
    url(r'^$', views.index),
    url(r'^logout/', views.logout),
    url(r'^register/', views.register),
    # blog url的分发

    url(r'^blog/', include('blog.url')),

    # media 配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # 配置关于文章添加中的文件上传路径，文本编辑器的指定路径
     url(r'^upload_file/', views.upload_file),
]
