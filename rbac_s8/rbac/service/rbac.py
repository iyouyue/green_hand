
from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import  redirect,HttpResponse,render

from django.contrib import auth

class M1(MiddlewareMixin):
    def process_request(self,request):

        print("1231231")
        "/orders/"
        #/admin/login/?next=/admin/
        # 当前访问路径  "/orders/"
        current_path = request.path_info

        valid_url_menu=["/login/","/reg/","/admin/.*","/$"]
        import re
        for valid_url in valid_url_menu:
            ret=re.match(valid_url,current_path) # /        /orders/

            if ret:
                return None

        #  验证用户是否登录
        user_id=request.session.get("user_id")
        print("user_id",user_id)
        if not user_id:
            return redirect("/login/")
        ###########################################################
        # 取出当前登录用户所有的权限列表
        # 方式1：
        # permission_list = request.session.get("permission_list")
        # 方式2
        permission_dict = request.session.get("permission_dict")

        # 匹配当前访问的url是否在当前用户的权限中
        # /users/edit/3
        import re
        '''
         permission_dict = {
            2: {
                  "urls": ["/orders/","/orders/add","/orders/delete/(\d+)"],
                  "codes": ["list","add","delete"]
            },
            1: {
                "urls": ["/users/",],
                "codes": ["list", ]
            },
        }

        '''
        for item in permission_dict.values():
            regs=item["urls"]
            codes=item["codes"]
            for reg in regs:
                reg="^%s$"%reg
                ret=re.match(reg,current_path)
                if ret:
                    request.permission_codes=codes
                    return None

        return HttpResponse("没有权限")








        # 方式1：
        # import re
        # flag = False
        # for permission_url in permission_list:
        #     permission_url="^%s$"%permission_url
        #     ret = re.match(permission_url, current_path)  # "^/orders/$"   /orders/add/
        #     if ret:
        #         flag = True
        #         break
        # if not flag:
        #     return HttpResponse("没有权限")
