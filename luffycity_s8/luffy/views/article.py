from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.core.exceptions import ObjectDoesNotExist

from luffy import models
from luffy.response.base import BaseResponse
from luffy.serializers.article import ArticleSerializer, ArticleDetailSerializer
from luffy.pagination.page import LuffyPageNumberPagination


class MyException(Exception):
    def __init__(self, msg):
        self.msg = msg


class ArticleView(GenericViewSet):
    renderer_classes = [JSONRenderer,]

    def list(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            # 1. 获取数据
            article_list = models.Article.objects.all().only('id', 'title','brief').order_by('-id')
            # 2. 对数据进行分页
            page = LuffyPageNumberPagination()
            page_article_list = page.paginate_queryset(article_list, request, self)
            # 3. 对数据序列化
            ser = ArticleSerializer(instance=page_article_list, many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 1001
            ret.error = '获取数据失败'
        return Response(ret.dict)

    def retrieve(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            obj = models.Article.objects.get(id=pk)
            ser = ArticleDetailSerializer(instance=obj, many=False)
            ret.data = ser.data
        except ObjectDoesNotExist as e:
            ret.code = 1001
            ret.error = '查询数据不存在'
        except Exception as e:
            ret.code = 1002
            ret.error = "查询失败"
        return Response(ret.dict)
