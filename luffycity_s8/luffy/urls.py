from django.conf.urls import url

from .views import course
from .views import price
from .views import article
from .views import comment
from .views import collection
from .views import auth

urlpatterns = [
    url(r'^degreecourse/$', course.DegreeCourseView.as_view({'get':'list'})),
    url(r'^degreecourse/(?P<pk>\d+)/$', course.DegreeCourseView.as_view({'get':'retrieve'})),

    url(r'^course/$', course.CourseView.as_view({'get':'list'})),
    url(r'^course/(?P<pk>\d+)/$', course.CourseView.as_view({'get':'retrieve'})),



    url(r'^article/$', article.ArticleView.as_view({'get': 'list'})),
    url(r'^article/(?P<pk>\d+)/$', article.ArticleView.as_view({'get': 'retrieve'})),

    url(r'^comment/$', comment.CommentView.as_view({'get': 'list','post':'create'})),
    url(r'^comment/(?P<pk>\d+)/$', comment.CommentView.as_view({'get': 'retrieve'})),
    url(r'^collection/$', collection.CollectionView.as_view({'get': 'list','post':'create'})),
    url(r'^collection/(?P<pk>\d+)/$', collection.CollectionView.as_view({'get': 'retrieve'})),

    url(r'^price/$', price.PriceView.as_view()),


    url(r'^auth/$', auth.AuthView.as_view()),

]
