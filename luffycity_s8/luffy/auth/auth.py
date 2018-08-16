from rest_framework.authentication import BaseAuthentication,exceptions
from luffy.models import *


class LuffyAuthentication(BaseAuthentication):

    def authenticate(self,request):
        token = request.query_params.get("token")
        token_obj = UserAuthToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed({'code':9999,'error':'认证失败'})
        return (token_obj.user, token_obj)




