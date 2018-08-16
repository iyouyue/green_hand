# from django.test import TestCase
#
# # Create your tests here.
#
#
#
# class Bird(object):
#
#     x=10
#     y=5
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age
#
#     def fly(self):
#         print(self.x)
#         print(self.y)
#         print("fly......")
#     def run(self):
#
#         print("Bird:run......")
#
#     def sing(self):
#         Bird.run(self)
#         print("singing......")
#
#
# class Qie(Bird):
#     def run(self):
#         print(self.y)
#         print("run......")
#     x=20
#
# # b=Bird("麻雀",23)
# # print(b.x)
# # b.fly()
#
# q=Qie("马化腾",48)
# # q.fly()
# #q.sing()
# q.sing()
#
#
#
# #############################
#
#
# #
# # class Person(object):
# #     def __init__(self,name,age):
# #         self.name=name
# #         self.age=age
# #
# # alex=Person("alex",33)
# #
# # # print(alex.name)
# # # print(alex.age)
# #
# # v=getattr(alex,"age")
# # print(v)
#



def foo():

    for i in range(1,100):
        yield i*i

for i in foo():
    print(i)



'''
 def inner(filter_field,current_id):
                 # temp = []
                 for obj in filter_field.get_data():
                     if isinstance(filter_field.filter_field_obj,ForeignKey) or isinstance(filter_field.filter_field_obj,ManyToManyField):
                         # link_tags=[]
                         import copy
                         params = copy.deepcopy(self.request.GET)
                         params._mutable = True
                         params[filter_field.filter_field_name]=obj.pk


                         if current_id==obj.pk:
                             yield mark_safe("<a class='active' href='?%s'>%s</a>" % (params.urlencode(), obj))
                         else:
                             yield mark_safe("<a href='?%s'>%s</a>" % (params.urlencode(), obj))
                     elif filter_field.filter_field_obj.choices:
                         # link_tags=[]
                         import copy
                         params = copy.deepcopy(self.request.GET)
                         params._mutable = True
                         params[filter_field.filter_field_name] = obj[0]

                         if current_id == obj[0]:
                             yield mark_safe("<a class='active' href='?%s'>%s</a>" % (params.urlencode(), obj[1]))
                         else:
                             yield mark_safe("<a href='?%s'>%s</a>" % (params.urlencode(), obj[1]))
                 else:
                     pass

                     #temp.append(data)
             yield inner(filter_field,current_id)
             # link_tags.append(temp)
         #print("link_tags",link_tags)
         #return link_tags





'''






