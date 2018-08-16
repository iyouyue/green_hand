from django.shortcuts import render,HttpResponse

# Create your views here.
from django.views import View
import json
from .models import *

# 为Book表创建序列化组件



# BOOK表所有数据   查看所有数据，添加一本书籍
# class BookView(APIView):
#
#     def get(self,request,*args,**kwargs):
#         book_list = Book.objects.all()
#
#         # 将QuerySet序列化成json数据
#         bs=BookSerializers(book_list,many=True,context={'request': request})
#         return Response(bs.data)
#     # 提交数据请求
#     def post(self,request,*args,**kwargs):
#         print(request.data)
#         # 将json数据转换为Queryset
#         bs=BookSerializers(data=request.data,context={'request': request})
#         if bs.is_valid():
#             bs.save()
#             # 数据保存成功
#             return Response(bs.data)
#         else:
#             return Response(bs.errors)

# 针对BOOK表某一个数据操作 查看，编辑，删除一本书

# class BookDetailView(APIView):
#     # 查看一本书
#     def get(self,request,pk,*args,**kwargs):
#         obj=Book.objects.filter(pk=pk).first()
#         if obj:
#             bs=BookSerializers(obj,context={'request': request})
#             return Response(bs.data)
#         else:
#             return Response()
#     # 编辑一本书
#     def put(self,request,pk,*args,**kwargs):
#         # obj :编辑书籍对象
#         obj = Book.objects.filter(pk=pk).first()
#         bs = BookSerializers(data=request.data,instance=obj,context={'request': request})
#         if bs.is_valid():
#             bs.save()
#             return Response(bs.data)
#         else:
#             return Response(bs.errors)
#
#     # 删除一本书
#     def delete(self,request,pk,*args,**kwargs):
#         Book.objects.filter(pk=pk).delete()
#         return Response()


# BOOK表所有数据   查看所有数据，添加一本书籍
# class PublishView(APIView):
#
#     def get(self,request,*args,**kwargs):
#         publish_list = Publish.objects.all()
#         # 将QuerySet序列化成json数据
#         bs=PublishSerializers(publish_list,many=True)
#         return Response(bs.data)
#     # 提交数据请求
#     def post(self,request,*args,**kwargs):
#         print(request.data)
#         # 将json数据转换为Queryset
#         bs=PublishSerializers(data=request.data)
#         if bs.is_valid():
#             bs.save()
#             # 数据保存成功
#             return Response(bs.data)
#         else:
#             return Response(bs.errors)
#
# # 针对BOOK表某一个数据操作 查看，编辑，删除一本书
#
# class PublishDetailView(APIView):
#     # 查看一本书
#     def get(self,request,pk,*args,**kwargs):
#         obj=Publish.objects.filter(pk=pk).first()
#         if obj:
#             bs=PublishSerializers(obj)
#             return Response(bs.data)
#         else:
#             return Response()
#     # 编辑一本书
#     def put(self,request,pk,*args,**kwargs):
#         # obj :编辑书籍对象
#         obj = Publish.objects.filter(pk=pk).first()
#         bs = PublishSerializers(data=request.data,instance=obj)
#         if bs.is_valid():
#             bs.save()
#             return Response(bs.data)
#         else:
#             return Response(bs.errors)
#
#     # 删除一本书
#     def delete(self,request,pk,*args,**kwargs):
#         Publish.objects.filter(pk=pk).delete()
#         return Response()


#===================================mixin=============================


# from rest_framework import mixins
# from rest_framework import generics
# class BookView(mixins.ListModelMixin,
#                mixins.CreateModelMixin,
#                generics.GenericAPIView):
#
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# class BookDetailView(
#     mixins.RetrieveModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.UpdateModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers
#
#     def get(self,request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def delete(self,request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#     def put(self,request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#
#
#
# from rest_framework import mixins
# from rest_framework import generics
# class PublishView(mixins.ListModelMixin,
#                mixins.CreateModelMixin,
#                generics.GenericAPIView):
#
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializers
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class PublishDetailView(
#     mixins.RetrieveModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.UpdateModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializers
#
#     def get(self,request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def delete(self,request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#     def put(self,request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#############################################使用通用的基于类######################

from rest_framework import mixins
from rest_framework import generics

# class BookView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers
#
# class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from api.service.serializers import *
from rest_framework.viewsets import  ModelViewSet
from api.service.auth import *

from api.service.permissions import SVIPPermission


from api.service.throttles import *
from api.service.page import *
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer

class BookViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer,BrowsableAPIRenderer]
    authentication_classes = [MyAuthentication,]
    permission_classes = [SVIPPermission]
    #throttle_classes = [VisitThrottle]
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    pagination_class = MyPageNumberPagination
    parser_classes = [JSONParser]




from rest_framework.parsers import  JSONParser,FormParser,FileUploadParser,MultiPartParser





class PublishView(generics.ListCreateAPIView):
    parser_classes = [FileUploadParser]
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers

    # def get(self, request, *args, **kwargs):
    #     publish_list=Publish.objects.all()
    #
    #     pnp=MyPageNumberPagination()
    #     pager_pulisher=pnp.paginate_queryset(queryset=publish_list,request=request,view=self)
    #     print("pager_pulisher",pager_pulisher)
    #     ps=PublishSerializers(pager_pulisher,many=True)
    #     return pnp.get_paginated_response(ps.data)
    #
    # # def post(self, request, *args, **kwargs):
    # #     print("data", request.data)
    # #     print("FILES", request.FILES)
    # #     return Response("OK123")

class PublishDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers

from .models import *
from django.http import JsonResponse

def get_random_str(user):
    import hashlib,time
    ctime=str(time.time())

    md5=hashlib.md5(bytes(user,encoding="utf8"))
    md5.update(bytes(ctime,encoding="utf8"))

    return md5.hexdigest()


class LoginView(APIView):
    authentication_classes = []
    def post(self,request,*args,**kwargs):
        user=request.data.get("user")
        pwd=request.data.get("pwd")
        user=User.objects.filter(user=user,pwd=pwd).first()
        res={"state_code":200,"msg":None}
        if user:
            random_str=get_random_str(user.user)
            user_token_obj=UserToken.objects.update_or_create(user=user,defaults={"token":random_str})
            res['msg']="success"
            res['token']=random_str
        else:
            res["msg"]="用户名或者密码错误"
            res["state_code"]=110

        return JsonResponse(res)






