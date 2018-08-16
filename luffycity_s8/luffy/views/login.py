from luffy.models import *
from django.http import JsonResponse
from rest_framework.views import APIView


# 获取随机字符串--token
def get_random_str(user):
    import hashlib, time
    ctime = str(time.time())
    md5 = hashlib.md5(bytes(user, encoding="utf8"))
    md5.update(bytes(ctime, encoding="utf8"))
    return md5.hexdigest()


class LoginView(APIView):
    # 登录不需要认证
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user = request.data.get("username")
        pwd = request.data.get("password")
        user = Account.objects.filter(username=user, password=pwd).first()
        # 设置认证返回状态码和返回信息
        res = {"state_code": 200, "msg": None}
        if user:
            random_str = get_random_str(user.username)
            UserAuthToken.objects.update_or_create(user=user, defaults={"token": random_str})
            res['msg'] = "认证成功"
            res['token'] = random_str
            res['user'] = user.username
        else:
            res["msg"] = "用户名或者密码错误"
            res["state_code"] = 110
        print(res)
        return JsonResponse(res)
