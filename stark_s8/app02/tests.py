from django.test import TestCase

# Create your tests here.

# def foo():
#     print("foo")
#
# print(callable(foo)) #True
#
# print(foo.__name__) # foo



#
# class Person(object):
#     def __init__(self,name):
#         self.name=name
#     def __str__(self):
#         return self.name
# alex=Person("alex")
#
# # print(alex.name)
#
# print(alex.__str__())




'''

 # 生成表表头  # header_list:  ["ID","标题","价格","操作"]
        # header_list=[]
        # for field in self.get_list_display(): # [checkbox,"__str__",edit,delete]
        #      if callable(field):
        #          #header_list.append(field.__name__)
        #          val=field(self,is_header=True)
        #          header_list.append(val)
        #      else:
        #          if field=="__str__":
        #              header_list.append(self.model._meta.model_name.upper())
        #          else:
        #              field_obj = self.model._meta.get_field(field)
        #              header_list.append(field_obj.verbose_name)

        # 生成表单数据列表
        # data_list=self.model.objects.all()  #  [obj1,obj2,....]
        print("self.list_display",self.list_display) # ["id","title",edit]
        new_data_list=[]
        for obj in data_list:
            temp=[]  #   [1,"python",111,"<a>编辑</a>"]
            for field in self.get_list_display():# [checkbox,"__str__",edit,delete]
                if callable(field):
                    val=field(self,obj)  # self.edit
                else:
                    val = getattr(obj, field)  # "__str__"
                    if field in self.list_display_links:
                        val=self.get_link_tag(obj,val)
                temp.append(val)

            new_data_list.append(temp)

        print("new_data_list",new_data_list)



         [
            obj1,
            obj2,
            obj3,

          ]

         list_display=["id","title","price"]

          [
              [1,"python",12,"<a>编辑</a>"],
              [2,"java",23,"<a>编辑</a>"],
              [3,"php",111,"<a>编辑</a>"],
          ]


self.request=request

        # 生成分页栏
        current_page = request.GET.get("page", 1)
        base_url = request.path_info
        params = request.GET
        from stark.utils.page import Pagination
        all_count = self.model.objects.all().count()
        pagination = Pagination(current_page, all_count, base_url, params, per_page_num=2, pager_count=11)

        data_list =self.model.objects.all()[pagination.start:pagination.end]

'''





# from .models import *
# from .apps import *
# from django.db.models import Q

# UserInfo.objects.filter(Q(name="yuan")|Q(email="123@qq.com"))
#
#
#
# q=Q()
# q.connector="or"
# q.children.append("name","yuan")
# q.children.append("email","123@qq.com")
# UserInfo.objects.filter(q)




# def foo():
#     print("foo")
#
# if __name__ == '__main__':
#
#     print(foo.__name__)
#     foo.desc="foo函数"
#     print(foo.desc)





class B(object):
    def __init__(self):
        pass
class A(B):
  pass

a=A()
b=B()
print(isinstance(a,A))
print(isinstance(a,B))

# print(type(a)==type(b))










