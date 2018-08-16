from rest_framework.views import APIView
from rest_framework.response import Response
from luffy.auth.auth import LuffyAuthentication
from rest_framework.request import Request
class PriceView(APIView):
    authentication_classes = [LuffyAuthentication,]
    def get(self,request,*args,**kwargs):
        print(request.user)
        print(request.auth)
        return Response('...')