
from rest_framework.throttling import BaseThrottle,SimpleRateThrottle

import time
VISITED_RECORD={}

# class VisitThrottle(BaseThrottle):
#     def __init__(self):
#         self.history=None
#
#     def allow_request(self,request,view):
#         print("ident",self.get_ident(request))
#         #visit_ip=request.META.get('REMOTE_ADDR')
#         visit_ip=self.get_ident(request)
#         print(visit_ip)
#         ctime=time.time()
#
#         #第一次访问请求
#         if visit_ip not in VISITED_RECORD:
#             VISITED_RECORD[visit_ip]=[ctime]
#             return True
#         # self.history：当前请求IP的记录列表
#         self.history = VISITED_RECORD[visit_ip]
#         print(self.history)
#
#         # 第2,3次访问请求
#         if len(VISITED_RECORD[visit_ip])<3:
#             VISITED_RECORD[visit_ip].insert(0,ctime)
#             return True
#
#         if ctime-VISITED_RECORD[visit_ip][-1]>60:
#             VISITED_RECORD[visit_ip].pop()
#             VISITED_RECORD[visit_ip].insert(0,ctime)
#             print("ok")
#             return True
#
#         return False
#
#
#     def wait(self):
#         import time
#         ctime = time.time()
#         return 60 - (ctime - self.history[-1])

class VisitThrottle(SimpleRateThrottle):
    scope = "xxxx"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
