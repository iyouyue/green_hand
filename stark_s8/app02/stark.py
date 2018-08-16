from stark.service.sites import site,ModelSatrk

from .models import *


class UserInfoconfig(ModelSatrk):
    pass
site.register(UserInfo,UserInfoconfig)



site.register(Role)
