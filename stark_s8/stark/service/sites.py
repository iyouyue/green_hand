
from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect

from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import ForeignKey,ManyToManyField



# 针对 （(),()）, [[],[]] 数据类型构建a标签

class LinkTagsGen(object):
    def __init__(self,data,filter_field,request):
        self.data=data   #  [(1,"python"),(2,"java")]
        self.filter_field=filter_field
        self.request = request


    def __iter__(self):

         from django.db.models import ForeignKey,ManyToManyField
         current_id = self.request.GET.get(self.filter_field.filter_field_name, 0)

         import copy
         params = copy.deepcopy(self.request.GET)
         params._mutable = True  # {"publish":1}
         if  params.get(self.filter_field.filter_field_name):
             del params[self.filter_field.filter_field_name]
             _url = "%s?%s" % (self.request.path_info, params.urlencode())
             yield mark_safe("<a href='%s'>全部</a>" % _url)
         else:
             yield mark_safe("<a class='active' href='#'>全部</a>")






         for item in self.data:   #   [(1,"python"),(2,"java")]    //   <QuerySet [<Publish: 人民出版社>, <Publish: 北京出版社>, <Publish: 江西出版社>]>  /// <QuerySet [<author: alex>, <author: egon>]>
             print("item",item)
             pk,text=None,None
             if self.filter_field.filter_field_obj.choices: # (2, '未出版')
                 pk,text=str(item[0]),item[1]
             elif  isinstance(self.filter_field.filter_field_obj,ForeignKey) or isinstance(self.filter_field.filter_field_obj,ManyToManyField):
                 pk, text = str(item.pk),item
             else:
                 pk, text = item[1], item[1]




             params[self.filter_field.filter_field_name]=pk

             _url="%s?%s"%(self.request.path_info,params.urlencode())
             if current_id==pk:
                 link_tag="<a class='active' href='%s'>%s</a>"%(_url,text)
             else:
                 link_tag="<a href='%s'>%s</a>"%(_url,text)


             yield mark_safe(link_tag)  #   <a href='?state=1'>已出版</a>






# 为每一个过滤的字段封装成整体类
class FilterField(object):
    def __init__(self,filter_field_name,filter_field_obj,config):
        self.filter_field_name=filter_field_name
        self.filter_field_obj=filter_field_obj
        self.config=config


    def get_data(self):
        if isinstance(self.filter_field_obj,ForeignKey) or isinstance(self.filter_field_obj,ManyToManyField):
            return self.filter_field_obj.rel.to.objects.all()
        elif self.filter_field_obj.choices:
            return self.filter_field_obj.choices
        else:
            return self.config.model.objects.values_list("pk",self.filter_field_name)




# ShowList服务于show_list_view
class ShowList(object):
    def __init__(self,config,request,queryset):
        self.request=request
        self.config=config
        self.queryset=queryset

        current_page = self.request.GET.get("page", 1)
        base_url = self.request.path_info
        params = self.request.GET
        from stark.utils.page import Pagination
        all_count =queryset.count()
        pagination = Pagination(current_page, all_count, base_url, params, per_page_num=2, pager_count=11)
        self.pagination=pagination
        data_list = self.queryset[pagination.start:pagination.end]
        self.data_list=data_list

        # actions
        self.actions=self.config.get_actions()  #  [patch_init,patch_delette]
        print("actions",self.actions)

        # filter
        self.list_filter=self.config.list_filter

    #   http://127.0.0.1:8000/admin/app01/book/?publish=1
    def get_filter_link_tags(self):


         for filter_field_name in self.list_filter: # ["state","publish","authors"]
             filter_field_obj = self.config.model._meta.get_field(filter_field_name)
             filter_field = FilterField(filter_field_name, filter_field_obj,self.config)

             print("filter_field",filter_field.get_data())
             val=LinkTagsGen(filter_field.get_data(),filter_field,self.request)

             yield val




    def handle_actions(self):

        temp=[]
        for action_func in self.actions:
            temp.append({"name":action_func.__name__,"desc":action_func.desc})

        return temp


    def get_header(self):
        header_list = []
        for field in self.config.get_list_display():  # [checkbox,"__str__",edit,delete]
            if callable(field):
                # header_list.append(field.__name__)
                val = field(self, is_header=True)
                header_list.append(val)
            else:
                if field == "__str__":
                    header_list.append(self.config.model._meta.model_name.upper())
                else:
                    field_obj = self.config.model._meta.get_field(field)
                    header_list.append(field_obj.verbose_name.upper())

        return header_list

    def get_body(self):
        # 生成表单数据列表
        # data_list=self.model.objects.all()  #  [obj1,obj2,....]
        print("self.list_display", self.config.list_display)  # ["id","title",edit]
        new_data_list = []
        for obj in self.data_list:
            temp = []  # [1,"python",111,"<a>编辑</a>"]
            for field in self.config.get_list_display():  # [checkbox,"__str__",edit,delete]
                if callable(field):
                    val = field(self.config, obj)  # self.edit
                else:

                    field_obj=self.config.model._meta.get_field(field)
                    if isinstance(field_obj,ManyToManyField):
                        ret=getattr(obj,field).all()
                        t=[]
                        for obj in ret:
                            t.append(str(obj))
                        val="-".join(t)
                        print(val)

                    else:
                        val = getattr(obj, field)  # "__str__"
                        if  field in self.config.list_display_links:
                             val = self.config.get_link_tag(obj, val)
                temp.append(val)

            new_data_list.append(temp)

        print("new_data_list", new_data_list)

        return new_data_list




class ModelSatrk(object):
    list_display = ["__str__",]

    model_form_class=None
    list_display_links=[]
    search_fields=[]
    actions=[]
    # 多级过滤
    list_filter=[]

    def __init__(self,model,site):
        self.model=model   # 用户访问的当前类
        self.site=site
        self.app_model_name=(self.model._meta.app_label, self.model._meta.model_name)



    def patch_delete(self,queryset):
        queryset.delete()
        return None

    patch_delete.desc="批量删除"

     # 获取真正展示的actions
    def get_actions(self):
        temp=[]
        temp.extend(self.actions)  #  [patch_init,patch_delete]
        temp.append(ModelSatrk.patch_delete)
        return temp






    # 获取当前查看表的编辑url
    def get_edit_url(self,obj):
        edit_url = reverse("%s_%s_change" % self.app_model_name, args=(obj.pk,))
        return edit_url

    #获取当前表的删除url
    def get_delete_url(self,obj):
        del_url = reverse("%s_%s_delete" % self.app_model_name, args=(obj.pk,))
        return del_url

    #获取当前查看表的添加页面的url
    def get_add_url(self):
        add_url = reverse("%s_%s_add" % self.app_model_name)
        return add_url

    # 获取当前查看表的查看页面的url
    def get_list_url(self):
        list_url = reverse("%s_%s_showlist" % self.app_model_name)
        return list_url

    #  编辑按钮
    def edit(self, obj=None, is_header=False):
        if is_header:
            return "操作"
        return mark_safe("<a href='%s'>编辑</a>" % self.get_edit_url(obj))
    # 删除按钮
    def delete(self, obj=None, is_header=False):
        if is_header:
            return "操作"
        return mark_safe("<a href='%s'>删除</a>" % self.get_delete_url(obj))
    # 复选框
    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return mark_safe("<input type='checkbox' id='action-toggle'>")

        return mark_safe("<input type='checkbox' name='_selected_action' value='%s'>" % obj.pk)


    # 获取真正展示的所有字段
    def get_list_display(self):
        new_list_dispaly=[]  #   [checkbox,"__str__",edit,delete]
        new_list_dispaly.extend(self.list_display)
        if not self.list_display_links:
            new_list_dispaly.append(ModelSatrk.edit)
        new_list_dispaly.append(ModelSatrk.delete)
        new_list_dispaly.insert(0,ModelSatrk.checkbox)
        return new_list_dispaly  #  [checkbox,"__str__",edit,delete]

    # 获取添加页面和编辑页面基于的ModelForm类
    def get_modelform_class(self):
        from django.forms import ModelForm
        from django.forms import widgets
        class ModelFormClass(ModelForm):
            class Meta:
                model = self.model
                fields = "__all__"

        if not self.model_form_class:
            return ModelFormClass
        else:
            return self.model_form_class

    # 获取编辑标签
    def get_link_tag(self,obj,val):
        params=self.request.GET
        import copy
        params=copy.deepcopy(params)
        params._mutable=True

        from django.http import QueryDict

        qd=QueryDict(mutable=True)

        qd["list_filter"]=params.urlencode()   # qd: {"list_filter":"a%21341%1234b%21322"}


        s=mark_safe("<a href='%s?%s'>%s</a>" % (self.get_edit_url(obj),qd.urlencode(),val))

        return s


    # 获取search的查询条件Q对象
    def get_search_condition(self):
        from django.db.models import Q
        search_condition = Q()
        search_condition.connector = "or"
        if self.search_fields:  # ["title","price"]
            key_word = self.request.GET.get("q")
            if key_word:
                for search_field in self.search_fields:
                    search_condition.children.append((search_field + "__contains", key_word))

        return search_condition

    def get_filter_condition(self):
        from django.db.models import Q
        fiter_condition = Q()
        for field ,val in self.request.GET.items():
            if field in self.list_filter:
                fiter_condition.children.append((field,val))

        return fiter_condition





    # 查看数据视图
    def show_list_view(self,request):

        # action操作
        if request.method=="POST":
            print("===",request.POST.get("action"))
            print("===",request.POST.getlist("_selected_action"))
            pk_list=request.POST.getlist("_selected_action")
            queryset=self.model.objects.filter(pk__in=pk_list)
            func_name=request.POST.get("action") #    "patch_init"
            func=getattr(self,func_name)
            ret=func(queryset)
            # return HttpResponse(ret)

        self.request = request

        # 关于search的模糊查询
        search_condition=self.get_search_condition()
        # action
        # 关于search的模糊查询
        #filter_condition = self.get_filter_condition()
        # filter的多级过滤
        get_filter_condition = self.get_filter_condition()

        queryset=self.model.objects.filter(search_condition).filter(get_filter_condition)

        sl=ShowList(self,request,queryset)

        add_url = self.get_add_url()
        return render(request,"stark/show_list.html",locals())
    # 添加数据视图
    def add_view(self,request):
        # 基于modelform

        ModelFormClass=self.get_modelform_class()
        if request.method=="GET":
            form=ModelFormClass()

            from django.forms.boundfield import BoundField
            from django.forms.models import ModelChoiceField


            for bound_field in form:   #  form组件下的每一个字段信息对象：bound_field
                #print("field",type(bound_field))
                #print(bound_field.name,bound_field.field)
                if isinstance(bound_field.field,ModelChoiceField):
                    bound_field.is_pop=True
                    #print(bound_field.field, type(bound_field.field))
                    print(bound_field.field.queryset.model)

                    app_label=bound_field.field.queryset.model._meta.app_label
                    model_name=bound_field.field.queryset.model._meta.model_name
                    _url="%s_%s_add"%(app_label,model_name)

                    bound_field.url=reverse(_url)+"?pop_id=id_%s"%bound_field.name

                else:
                    bound_field.is_pop = False
                    bound_field.url=None



            return render(request,"stark/add_view.html",{"form":form})
        else:
            form = ModelFormClass(data=request.POST)
            if form.is_valid():
                obj=form.save()
                pop_id=request.GET.get("pop_id")

                if pop_id:
                    res={"pk":obj.pk,"text":str(obj),"pop_id":pop_id}
                    import json
                    return render(request,"stark/pop_res.html",{"res":json.dumps(res)})
                return redirect(self.get_list_url())
            else:
                return render(request, "stark/add_view.html", {"form": form})

    # 编辑数据视图
    def change_view(self,request,id):
        # 基于modelform
        print("self.model", self.model)
        edit_obj=self.model.objects.filter(pk=id).first()
        ModelFormClass = self.get_modelform_class()
        if request.method=="GET":
            form=ModelFormClass(instance=edit_obj)
            return render(request,"stark/change_view.html",{"form":form})
        else:
            form=ModelFormClass(data=request.POST,instance=edit_obj)
            if form.is_valid():
                form.save()


                params=request.GET.get("list_filter")

                print("=====",params)
                url="%s?%s"%(self.get_list_url(),params)
                return redirect(url)
                #return redirect(self.get_list_url())
            else:
                return render(request, "stark/change_view.html", {"form": form})


    # 删除数据视图
    def del_view(self,request,id):
        del_obj = self.model.objects.filter(pk=id).first()
        if request.method=="GET":
            print("self.model", self.model)

            list_url=self.get_list_url()
            return render(request,"stark/del_view.html",{"del_obj":del_obj,"list_url":list_url})
        else:
            del_obj.delete()
            return redirect(self.get_list_url())






    # 设计url，二级分发
    def get_urls(self):
        temp = []
        model_name=self.model._meta.model_name
        app_label=self.model._meta.app_label
        app_model=(app_label,model_name)
        temp.append(url("^$", self.show_list_view,name="%s_%s_showlist"%app_model))
        temp.append(url("^add/$", self.add_view,name="%s_%s_add"%app_model))
        temp.append(url("^(\d+)/change/$", self.change_view,name="%s_%s_change"%app_model))
        temp.append(url("^(\d+)/delete/$", self.del_view,name="%s_%s_delete"%app_model))

        return temp

    @property
    def urls(self):
        return self.get_urls()


class StarkSite(object):

    def __init__(self):
        self._registry={}

    def register(self,model,model_config=None):
        if not model_config:
            model_config=ModelSatrk
        self._registry[model]=model_config(model,self)

    def get_urls(self):

        temp=[]
        for model,model_config in self._registry.items():
            model_name=model._meta.model_name
            app_label=model._meta.app_label
            u=url("^%s/%s/"%(app_label,model_name),(model_config.urls,None,None))
            temp.append(u)
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None

site=StarkSite()