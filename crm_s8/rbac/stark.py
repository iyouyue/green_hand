

from .models import *

from stark.service.sites import site,ModelSatrk



site.register(User)
site.register(Role)
site.register(Permission)
site.register(PermissionGroup)
site.register(Menu)