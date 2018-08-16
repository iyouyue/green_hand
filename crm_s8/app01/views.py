from django.shortcuts import render,redirect,HttpResponse

# Create your views here.

from rbac import models

def login(request):
    if request.method=="GET":
        return render(request,"login.html")

    else:
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        user=models.User.objects.filter(name=user,pwd=pwd).first()
        if user:
            # 验证成功之后做什么？

            request.session["user_info"]={"user_id":user.pk,"username":user.userinfo.username}
            # 当前登录用户的所有权限
            from rbac.service.initial import initial_session
            initial_session(request,user)

            return redirect("/index/")
        else:
            return redirect("/login/")


def index(request):

    return render(request,"index.html")