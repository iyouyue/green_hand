from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
# from utils.random_code import *


from django.contrib import auth
from .models import *
def log_in(request):
    if request.is_ajax():
        print(request.POST)
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        valid_code=request.POST.get("valid_code")
        code_str=request.session.get("random_code_str")
        '''
        1 sessionID=request.COOKIE.get("sessionID) # 123456abc
        2 django-session表
           session-key   session-data
           123456abc      {"random_code_str":"abc12"}
           360000abc      {"random_code_str":"abc45"}
           obj=django-session.objects.filter(session-key=123456abc)
        3  obj.session-data.get("random_code_str")  # abc12
        '''
        print("random_code_str",code_str)

        login_response={"user":None,"error_msg":""}

        if valid_code.upper()==code_str.upper():
            user=auth.authenticate(username=user,password=pwd)
            if user:
                login_response["user"]=user.username
                auth.login(request,user) # 1  {"user_id":1}  2 request.user=user
                print("===",request.session.get("random_code_str"))
            else:
                login_response["error_msg"] ="username or password error!"
        else:
            login_response["error_msg"]="valid code error!"

        import json
        return HttpResponse(json.dumps(login_response))

    return render(request,"login.html")

# 构建查询分类数据
# def get_achive(username):
#     user = UserInfo.objects.filter(username=username).first()
#     # 当前站点
#     blog = user.blog
#     # 查询当前站点的所有分类
#     # category_list=Category.objects.filter(blog=blog)
#     # category_list=Category.objects.filter(blog_id=blog.pk)
#     from django.db.models import Count
#     # 查询每一个分类名称以及对应的文章数
#     # Category.objects.all().annotate(c=Count("article")).values_list("title","c")
#     cate_list = Category.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
#     # print(ret)
#
#     # 查询但当前站点每一个标签名称以及对应的文章数
#     tag_list = Tag.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
#     print(tag_list)
#
#     # 日期归档   [["2018-02",5],["2010-9",6]]
#     date_ist = Article.objects.filter(user=user) \
#         .extra(select={"create_time_ym": "strftime('%%Y/%%m',create_time)"}) \
#         .values("create_time_ym") \
#         .annotate(c=Count("nid")).values_list("create_time_ym", "c")
#
#     return {"cate_list":cate_list,"tag_list":tag_list,"date_ist":date_ist}

def index(request):
    print("random_code_str",request.session.get("random_code_str"))
    article_list=Article.objects.all()
    return render(request,"index.html",locals())

def logout(request):
    auth.logout(request)
    print("---",request.session.get("random_code_str"))
    #request.session.flush()
    return redirect("/login/")

def get_valid_img(request):
    '''
    :param request:
    :get_valid_img: 生成验证码，返回图片数据
    :return:
    '''

    from blog.utils.valid_code import get_valid_img
    info=get_valid_img(request)

    request.session["random_code_str"] = "".join(info[1])
    # request.session["a"]="pp"
    # request.session["3"]="bbbnnnnnnnn"
    # del request.session["random_code_str"]
    '''
    if cookie.get(sesssion):更新

    1 生成随机字符串
    2 响应set_cookie {"sessionId":"123456abc"}
    3 在django-session表中插入一条记录
       session-key   session-data
       123456abc      {"random_code_str":"abc12"}
    '''

    return HttpResponse(info[0])

from blog.forms import RegisterForm

def register(request):
    if request.is_ajax():
        register_form = RegisterForm(request.POST)

        reg_response={"user":None,"error_msg":None}
        if register_form.is_valid():
            user=register_form.cleaned_data.get("user")
            pwd=register_form.cleaned_data.get("pwd")
            email=register_form.cleaned_data.get("email")
            avatar_obj=request.FILES.get("avatar") # 图片对象
            if avatar_obj:
                user_obj=UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=avatar_obj)
            else:
                user_obj=UserInfo.objects.create_user(username=user,password=pwd,email=email)

            reg_response["user"]=user_obj.username
        else:
            reg_response["error_msg"]=register_form.errors
        import json
        return HttpResponse(json.dumps(reg_response))

    register_form=RegisterForm()
    return render(request,"register.html",{"register_form":register_form})

####个人站点： home_site

def home_site(request,username,**kwargs):
    print(kwargs)
    #  判断用户是否存在
    user=UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request,"blog/not_found.html")

    #Article.objects.filter(user_id=user.pk)
    if not kwargs:
         # 筛选当前站点的所有文章
         article_list=Article.objects.filter(user=user)
    else:
        # 归档跳转标签的请求，对article_list过滤
        condition=kwargs.get("condition") # {'condition': 'cate', 'params': 'yuan的python'}
        params=kwargs.get("params")
        if condition=="cate":
            article_list = Article.objects.filter(user=user).filter(homeCategory__title=params)
        elif condition=="tag":
            article_list = Article.objects.filter(user=user).filter(tags__title=params)
        else:
            year,month=params.split("/")
            article_list = Article.objects.filter(user=user).filter(create_time__year=year,create_time__month=month)


    return render(request,"blog/home_site.html",locals())

def article_detail(request,username,article_id):

    article_obj=Article.objects.filter(pk=article_id).first()

    comment_list=Comment.objects.filter(article_id=article_id)


    # 思路1：
    # 构建评论树
    comment_tree=Comment.objects.filter(article_id=article_id).values("nid","content","parent_comment_id")
    for obj in comment_tree:
        obj["children_list"] = []

    ret = []
    for obj in comment_tree:
        pid = obj["parent_comment_id"]
        if pid:
            for i in comment_tree:
                if i["nid"] == pid:
                    i["children_list"].append(obj)
        else:
            ret.append(obj)

    print(ret)


    return render(request,"blog/article_detail.html",{"username":username,"article_obj":article_obj,"comment_list":comment_list})

#############文章详细页
from django.db.models import F
from django.db import transaction

from django.http import JsonResponse
import json
def digg(request):
    print(request.POST)
    article_id=request.POST.get("article_id")
    is_up=json.loads(request.POST.get("is_up")) #  "true"
    user_id=request.user.pk
    response={"state":True}
    try:
        with transaction.atomic(): #  事务处理
            obj=ArticleUpDown.objects.create(user_id=user_id,article_id=article_id,is_up=is_up)
            if is_up:
                Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
            else:
                Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
    except Exception as e:
        first_updown=ArticleUpDown.objects.filter(user_id=user_id,article_id=article_id).values("is_up").first().get("is_up")
        response["state"]=False
        response["first_updown"]=first_updown

    return JsonResponse(response)

def comment(request):
     content=request.POST.get("content")
     article_id=request.POST.get("article_id")
     user_id=request.user.pk  #  登录对象即是评论对象
     pid=request.POST.get("pid")

     comment_resonse={}
     with transaction.atomic():
         if pid:  #  子评论
             comment=Comment.objects.create(content=content,article_id=article_id,user_id=user_id,parent_comment_id=pid)
         else:   #   根评论
             comment = Comment.objects.create(content=content, article_id=article_id, user_id=user_id)

         Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)

     comment_resonse["create_time"]=comment.create_time.strftime("%Y-%m-%d %H:%M")
     comment_resonse["content"]=comment.content

     import json

     return HttpResponse(json.dumps(comment_resonse))

def backend(request,username):

    article_list=Article.objects.filter(user__username=username)

    return render(request,"blog/backend_index.html",{"username":username,"article_list":article_list})

def backend_add_article(request,username):
    if request.method=="POST":
        content=request.POST.get("content")

        # 用BS模块过滤content，

        valid_tags_attrs_list={
            "div":["id","class","style"],
            "img":["src","width","height"],
            "a":["href"],
            "p":[],

        }

        from bs4 import BeautifulSoup

        soup=BeautifulSoup(content,'html.parser')
        tags_list=soup.find_all()

        for tag in tags_list:
            print(tag.name)
            # print(tag.attrs)
            if tag.name not in valid_tags_attrs_list:
                tag.decompose()

        print("content:",soup)








    return render(request,"blog/backend_add_article.html")


def upload_file(request):
    print(request.FILES)
    # 保存上传到指定路径
    obj=request.FILES.get("upload_img")
    print(type(obj))

    from django.core.files.uploadedfile import InMemoryUploadedFile
    from s8_cnblog import settings
    import os
    path=os.path.join(settings.MEDIA_ROOT,"article_imgs",obj.name)
    with open(path,"wb") as f_write:

        for chunk in obj.chunks():
            f_write.write(chunk)
    # 给本文编辑器返回json字符串

    upload_response={
        "error":0,
        "url":"/media/article_imgs/%s"%obj.name
    }

    import json


    return HttpResponse(json.dumps(upload_response))


def get_comment_tree(request,article_id):


     conmment_list=list(Comment.objects.filter(article_id=article_id).values("nid","content","parent_comment_id","user__username"))

     from django.http import JsonResponse

     return JsonResponse(conmment_list,safe=False)