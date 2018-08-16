

from rest_framework.permissions import BasePermission

class SVIPPermission(BasePermission):

    message="您没有访问权限"
    def has_permission(self,request,view):

        if request.user.user_type==3:
            return True
        else:
            return False
