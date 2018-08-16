from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from rbac.models import *
def login(request):
    if request.method=="GET":
        return render(request,"login.html")

    else:
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        user=UserInfo.objects.filter(name=user,pwd=pwd).first()
        if user:
            # 验证成功之后做什么？

            request.session["user_id"]=user.pk
            # 当前登录用户的所有权限
            from rbac.service.initial import initial_session
            initial_session(request,user)


            #  {"user_id":1,"permission_list":['/users/','/orders/']}
            return HttpResponse("登录成功！")
        else:
            return redirect("/login/")

from rbac.service.base import *


class UserPermissions(Permissions):
    def xxxx(self):
        return "xxxx" in self.code_list

def users(request):
    # print(request.session["permission_list"])


    return render(request,"users.html",locals())




def orders(request):


    permission_codes=request.permission_codes  #    ["list","add"]
    print(permission_codes)

    per=Permissions(permission_codes)

    # print(request.session["permission_list"])


    return render(request,"orders.html",locals())


def order_add(request):

    return HttpResponse("添加订单")


######################################################33

def m1(request):
    #print(request.session["permission_list"])
    permission_list=request.session["permission_list"]

    #############temp_dict:存储所有放到菜单栏中的权限
    temp_dict={}
    for item in permission_list:
        pid=item["pid"]
        if not pid:
            item["active"]=False
            temp_dict[item["id"]]=item

    #print(temp_dict)


    #######将需要标中的active设置True
    current_path = request.path_info
    import re
    for item in permission_list:
        pid = item["pid"]
        url = "^%s$" % item["url"]
        if re.match(url, current_path):
            if pid:
                temp_dict[pid]["active"] = True
            else:
                item["active"] = True

    ########将temp_dict转换为最终的menu_dict的数据格式

    menu_dict = {}
    for item in temp_dict.values():

        if item["menu_id"] in menu_dict:

            temp = {"title": item["title"], "url": item["url"], "active": item["active"]},
            menu_dict[item["menu_id"]]["children"].append(temp)

            if item["active"]:
                menu_dict[item["menu_id"]]["active"] = True
        else:

            menu_dict[item["menu_id"]] = {

                "title": item["menu_name"],
                "active": item["active"],
                "children": [
                    {"title": item["title"], "url": item["url"], "active": item["active"]},
                ]

            }
    print(menu_dict)
    return render(request,"m1.html",locals())


def m2(request):

    return render(request,"m2.html")
