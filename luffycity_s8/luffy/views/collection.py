from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.core.exceptions import ObjectDoesNotExist

from luffy import models
from luffy.response.base import BaseResponse
from luffy.serializers.collection import CollectionSerializer, CollectionDetailSerializer
from luffy.pagination.page import LuffyPageNumberPagination


class MyException(Exception):
    def __init__(self, msg):
        self.msg = msg


class CollectionView(GenericViewSet):
    renderer_classes = [JSONRenderer,]

    def list(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            # 1. 获取数据
            collection_list = models.Collection.objects.all().only('id', 'content_type_id').order_by('-id')
            # 2. 对数据进行分页
            page = LuffyPageNumberPagination()
            page_collection_list = page.paginate_queryset(collection_list, request, self)
            # 3. 对数据序列化
            ser = CollectionSerializer(instance=page_collection_list, many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 1001
            ret.error = '获取数据失败'
        return Response(ret.dict)

    def retrieve(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            obj = models.Collection.objects.get(id=pk)
            ser = CollectionDetailSerializer(instance=obj, many=False)
            ret.data = ser.data
        except ObjectDoesNotExist as e:
            ret.code = 1001
            ret.error = '查询数据不存在'
        except Exception as e:
            ret.code = 1002
            ret.error = "查询失败"
        return Response(ret.dict)

    def create(self, request, *args, **kwargs):
        ret = BaseResponse()
        collection_serializer = CollectionDetailSerializer(data=request.data)
        if collection_serializer.is_valid():
            collection_serializer.save()
            ret.data = collection_serializer.data
        else:
            ret.code = 1010
            ret.error = "添加失败"
        return Response(ret.dict)
