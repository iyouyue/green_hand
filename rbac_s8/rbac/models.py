from django.db import models

# Create your models here.

class Menu(models.Model):
    caption=models.CharField(max_length=32)

    def __str__(self):
        return self.caption

class UserInfo(models.Model):
    name=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32,default=123)
    email=models.EmailField()
    roles=models.ManyToManyField(to="Role")

    def __str__(self):
        return self.name

class Role(models.Model):
    title=models.CharField(max_length=32)
    permissions=models.ManyToManyField(to="Permission")
    def __str__(self):
        return self.title

class Permission(models.Model):
    url=models.CharField(max_length=32)
    title=models.CharField(max_length=32)
    permission_group=models.ForeignKey("PermissionGroup",default=1)
    code=models.CharField(max_length=32,default="")
    parent=models.ForeignKey("self",default=1,null=True,blank=True)
    def __str__(self):
        return self.title

class PermissionGroup(models.Model):
    caption=models.CharField(max_length=32)
    menu=models.ForeignKey("Menu",default=1)
    def __str__(self):
        return self.caption