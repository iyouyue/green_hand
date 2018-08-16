from django.test import TestCase

# Create your tests here.


# import datetime
# datetime.date   : "年月日"
#
# datetime.time   ： "时分秒"
#
# datetime.datetime："年月日 时分秒"
#
# datetime.timedelta："构建时间对象"

import datetime

# datetime.timedelta
#
# print(datetime.datetime.now())  # 2018-02-08 11:44:02.382526
# date_obj=datetime.datetime.now()
# print(date_obj.year)
# print(date_obj.month)
# print(date_obj.day)
# print(date_obj.second)
# print(date_obj.hour)
# print(date_obj.weekday())

# import requests
#
# res=requests.get('http://www.cnblogs.com/yuanchenqi/articles/7617280.html')
# print(res.text)

##################################BS模块的使用: 针对标签字符串做操作

# from bs4 import BeautifulSoup
#
# s= """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
#
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
# and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.
# <div egon="123">1231</div>
# </p>
#
# <p class="story">...</p>




# s='''
# <div class='c1'>
#     <div class='c2'>c22222
#         <div class='c4'>c44444</div>
#     </div>
# </div>
# <div class='c1'><div class='c3'>c33333</div></div>
# <div class='c1'>3333</div>
# <p class='p1'>4444</p>
#
#
# '''

# soup=BeautifulSoup(s,"html.parser")


#  soup对象提供的查询方法   :  标签就是一个对象   tag.属性  tag.方法

# soup.标签名：第一个该名称的标签对象
# print(soup.a.name)     # "a"
# print(soup.a.string)  # Elsie
# print(soup.a.text)    # Elsie
# print(soup.a.parent.name)    # Elsie
# print(soup.a["class"])    # Elsie
# print(soup.a["href"])    # Elsie

#   find 与find_all ： 找标签

# print(soup.find_all('a'))
# for link_tag in soup.find_all("a"):
#     print(link_tag["href"])

# print(soup.find("a")["href"])   # 等效soup.a
# print(soup.find_all("div"))   # 等效soup.a

# print(soup.find("a")["href"])
# print(soup.find("a").get("href"))

#   找属性和标签名称
#
# print(soup.a.name)
# #print(soup.a["属性名"])
# print(soup.a.attrs)  # 字典 {"class":["",""],"id":1}
# print(soup.a.attrs.get("href"))


#  对处理的标签字符串修改操作

# soup.a.attrs["class"]=1111
# soup.a["class"]=222
# del soup.a['class']
# print(soup.a)
#
#
# #  查询标签文本  text  string
#
# print(soup.a.string)
# print(soup.find("p","story").string)
# print(soup.find("p","story").text)




#  导航查找 XXXXXXXXXXXXXXXXXXXXX

#print(soup.find("p","story").contents)
# print(soup.find("p","story").children)
# for obj in soup.find("p","story").children:
#     print("======")
#     print(obj)

#print(soup.find("p","story").parent.name)
# print(soup.find("p","story").next_element,"===")

###########find()  find_all()  find_all( name , attrs , recursive , string , **kwargs )


# print(soup.find("div",{"egon":123}))
#
# soup.select("#id .class")


#===================可变数据类型=================
# 在python中可变数据类型   列表  字典
# 在python中不可变数据类型 数字  元组  字符串


# s="hello"
# s.upper()
# print(s)


# l=[111,222]
# l.append(333)
# print(l)


# l1=[11,222]
# l2=[333,444,l1]
#
# l1.append(555)
# print(l1)
# print(l2)

# d={1:{"xxx":[1,2,3,]},2:{"xxx":[4,5,6,[7,8,9]]},3:{"xxx":[7,8,9]}}
#
# d[1]["xxx"].append(d[2]["xxx"])
# d[2]["xxx"].append(d[3]["xxx"])

# 字典生成式
# a=[i*i for i in [11,22,33,]]  # 列表生成式
# print(a)
#
# b={ i:i*i for i in [111,222,333]}
# print(b)
#
# d={"1":111,"2":222}
#
# d={ value:key for key,value in d.items()}
# print(d)

#  结论：  一旦某个数据引用了一个可变数据类型，可变数据类型发生变化，该数据跟着发生变化
# 111
#    444
#       666
#    555
# 222
# 333
#    777
#       888
# 999

comment_list=[

    {"id":1,"content":"111","Pid":None},
    {"id":2,"content":"222","Pid":None},
    {"id":3,"content":"333","Pid":None},
    {"id":4,"content":"444","Pid":1},
    {"id":5,"content":"555","Pid":1},
    {"id":6,"content":"666","Pid":4},
    {"id":7,"content":"777","Pid":3},
    {"id":8,"content":"888","Pid":7},
    {"id":9,"content":"999","Pid":None},

]







for obj in comment_list:
    obj["children_list"]=[]


ret=[]
for obj in comment_list:
    pid=obj["Pid"]
    if pid:
        for i in comment_list:
            if i["id"]==pid:
                i["children_list"].append(obj)
    else:
        ret.append(obj)

print(ret)

'''

comment_list=[

    {"id":1,"content":"111","Pid":None，"children_list":[id=4 引用，id=5 引用]},
    {"id":2,"content":"222","Pid":None，"children_list":[]},
    {"id":3,"content":"333","Pid":None，"children_list":[{"id":7,"content":"777","Pid":3，"children_list":[]}]},
    {"id":4,"content":"444","Pid":1，"children_list":[id=6引用]},
    {"id":5,"content":"555","Pid":1，"children_list":[]},
    {"id":6,"content":"666","Pid":4，"children_list":[]},
    {"id":7,"content":"777","Pid":3，"children_list":[{"id":8,"content":"888","Pid":7，"children_list":[]}]},
    {"id":8,"content":"888","Pid":7，"children_list":[]},
    {"id":9,"content":"999","Pid":None，"children_list":[]},

]


ret=[
{"id":1,"content":"111","Pid":None,"children_list":[{"id":4,"content":"444","Pid":1，"children_list":[{"id":6,"content":"666","Pid":4，"children_list":[]}，]},{"id":5,"content":"555","Pid":1，"children_list":[]},]}     #  引用
{"id":2,"content":"222","Pid":None,"children_list":[]},    #  引用
{"id":3,"content":"333","Pid":None，"children_list":[{"id":7,"content":"777","Pid":3，"children_list":[{"id":8,"content":"888","Pid":7，"children_list":[]}，]}]},    #  引用
{"id":9,"content":"999","Pid":None，"children_list":[]}
]
s=''
111
   444
222
    555
       666
333''

'''






































