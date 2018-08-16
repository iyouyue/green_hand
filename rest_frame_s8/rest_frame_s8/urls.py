"""rest_frame_s8 URL Configuration

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



from api import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # url(r"books\.(?P<format>\w+)$",views.BookViewSet.as_view({"get":"list","post":"create"}),name="book_list"),
    # url(r"books/$",views.BookViewSet.as_view({"get":"list","post":"create"}),name="book_list"),
    # url(r"books/(?P<pk>\d+)/$",views.BookViewSet.as_view({"get":"retrieve","delete":"destroy","put":"update"}),name="book_detail"),
    # url(r"books/(?P<pk>\d+)\.(?P<format>\w+)$",views.BookViewSet.as_view({"get":"retrieve","delete":"destroy","put":"update"}),name="book_detail"),

    url(r'^', include(router.urls)),

    url(r"publishes/$",views.PublishView.as_view(),name="publish_list"),
    url(r"publishes/(?P<pk>\d+)/$",views.PublishDetailView.as_view(),name="publish_detail"),

    url("login/$",views.LoginView.as_view())
]
