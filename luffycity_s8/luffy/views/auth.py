from rest_framework.views import APIView
from rest_framework.response import Response
class AuthView(APIView):

    def post(self,request,*args,**kwargs):
        print(request.data)
        return Response('.........')