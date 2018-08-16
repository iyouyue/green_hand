from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.versioning import URLPathVersioning
from django.core.exceptions import ObjectDoesNotExist

from luffy import models
from luffy.response.base import BaseResponse
from luffy.serializers.course import DegreeCourseSerializer, DegreeCourseDetailSerializer,CourseSerializer, CourseDetailSerializer
from luffy.pagination.page import LuffyPageNumberPagination


class MyException(Exception):
    def __init__(self, msg):
        self.msg = msg


class DegreeCourseView(GenericViewSet):
    """
    学位课相关接口
    """
    def list(self, request, *args, **kwargs):
        """
        查看学位课列表
        :param request: 请求相关所有数据
        :param args: url中传入的参数
        :param kwargs:url中传入的参数
        :return:  封装了响应相关的所有数据Response对象
        """
        ret = BaseResponse()
        try:
            # 1. 获取数据
            course_list = models.DegreeCourse.objects.all().only('id', 'name').order_by('-id')
            # 2. 对数据进行分页
            page = LuffyPageNumberPagination()
            page_course_list = page.paginate_queryset(course_list, request, self)
            # 3. 对数据序列化
            ser = DegreeCourseSerializer(instance=page_course_list, many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 1001
            ret.error = '获取数据失败'
        return Response(ret.dict)

    def retrieve(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            obj = models.DegreeCourse.objects.get(id=pk)
            ser = DegreeCourseDetailSerializer(instance=obj, many=False)
            ret.data = ser.data
        except ObjectDoesNotExist as e:
            ret.code = 1001
            ret.error = '查询数据不存在'
        except Exception as e:
            ret.code = 1002
            ret.error = "查询失败"
        return Response(ret.dict)


class CourseView(GenericViewSet):

    def list(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            # 1. 获取数据
            # course_list = models.Course.objects.all().exclude(course_type=3).only('id', 'name').order_by('-id')

            # course_type = request.query_params.get('course_type')
            # course_list = models.Course.objects.all().filter(course_type=course_type).only('id', 'name').order_by('-id')

            course_type = request.query_params.getlist('course_type')
            course_list = models.Course.objects.all().filter(course_type__in=course_type).only('id', 'name').order_by('-id')

            # 2. 对数据进行分页
            page = LuffyPageNumberPagination()
            page_course_list = page.paginate_queryset(course_list, request, self)
            # 3. 对数据序列化
            ser = CourseSerializer(instance=page_course_list, many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 1001
            ret.error = '获取数据失败'
        return Response(ret.dict)

    def retrieve(self, request, pk, *args, **kwargs):
        ret = BaseResponse()
        try:
            obj = models.Course.objects.get(id=pk)
            ser = CourseDetailSerializer(instance=obj, many=False)
            ret.data = ser.data
        except ObjectDoesNotExist as e:
            ret.code = 1001
            ret.error = '查询数据不存在'
        except Exception as e:
            ret.code = 1002
            ret.error = "查询失败"
        return Response(ret.dict)