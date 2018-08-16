

from django.utils.safestring import mark_safe
from django.conf.urls import url
from stark.service.sites import site,ModelSatrk
from django.shortcuts import  HttpResponse,redirect,render
from .models import *

site.register(Department)

class UserConfig(ModelSatrk):
    list_display = ["name","email","depart"]
    list_display_links = ["name"]
site.register(UserInfo,UserConfig)

site.register(Course)

class SchoolConfig(ModelSatrk):
    list_display = ["id","title"]
    list_display_links=["title"]

site.register(School,SchoolConfig)

class ClassListconfig(ModelSatrk):

    def display_class(self,obj=None,is_header=False):
        if is_header:
            return "班级"
        return "%s(%s)"%(obj.course,obj.semester)

    list_display = [display_class,"teachers","tutor",]
site.register(ClassList,ClassListconfig)

class CustomerConfig(ModelSatrk):
    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return "性别"
        return obj.get_gender_display()

    def display_status(self,obj=None,is_header=False):
        if is_header:
            return "状态"
        return obj.get_status_display()

    def display_courses(self, obj=None, is_header=False):
        if is_header:
            return "咨询课程"
        temp=[]
        for course in obj.course.all():
            tag="<a href='/stark/app01/customer/cancel/%s/%s' style='padding:6px 3px;border:1px solid #336699'>%s</a>"%(obj.pk,course.pk,course.name)
            temp.append(tag)
        s="".join(temp)
        return mark_safe(s)

    def cancel_course(self,request,customer_id,course_id):

        customer=Customer.objects.get(pk=customer_id)
        customer.course.remove(course_id)

        return redirect(self.get_list_url())

    def public_customers(self,request):

        from django.db.models import Q
        import datetime
        current_date=datetime.datetime.now()
        delta_15d=datetime.timedelta(days=15)
        delta_3d=datetime.timedelta(days=3)


        # 15天未成单，或者三天未跟进的客户属于公共客户

        #15天未成单:  current_date-recv_date>15------>recv_date<current_date-15

        #三天未跟进:  current_date-last_consult_date>3

        user_id=3
        customer_list=Customer.objects.filter(Q(recv_date__lt=current_date-delta_15d)|Q(last_consult_date__lt=current_date-delta_3d),status=2).exclude(consultant_id=user_id)

        return render(request,"public_customers.html",locals())

    def mycustormers(self,request):
        user_id=3

        customer_distrbute_list=CustomerDistrbute.objects.filter(consultant_id=user_id)

        return render(request,"mycustomers.html",locals())

    def further_follow(self,request,customer_id):

        user_id=4
        import datetime
        cdate=datetime.datetime.now()
        from django.db.models import Q

        import datetime
        current_date = datetime.datetime.now()
        delta_15d = datetime.timedelta(days=15)
        delta_3d = datetime.timedelta(days=3)

        ret=Customer.objects.filter(pk=customer_id).filter(Q(recv_date__lt=current_date-delta_15d)|Q(last_consult_date__lt=current_date-delta_3d)).update(consultant_id=3,recv_date=cdate,last_consult_date=cdate)
        if not ret:
            return HttpResponse("没了")
        CustomerDistrbute.objects.create(customer_id=customer_id,consultant_id=user_id,date=cdate,status=1)

        return HttpResponse("抢单成功！")

    def extra_url(self):

        temp=[]
        temp.append(url("cancel/(\d+)/(\d+)/$", self.cancel_course))
        temp.append(url("public/$", self.public_customers))
        temp.append(url("mycustormers/$", self.mycustormers))
        temp.append(url("further_follow/(\d+)$", self.further_follow))

        return temp


    def display_consultrecord(self,obj=None,is_header=False):
        if is_header:
            return "跟进"
        return mark_safe("<a href='/stark/app01/consultrecord/?customer=%s'>跟进记录</a>"%(obj.pk))


    list_display = ["name",display_gender,"consultant",display_courses,display_status,display_consultrecord]

    list_display_links = ["name"]


site.register(Customer,CustomerConfig)

class ConsultRecordConfig(ModelSatrk):
    list_display = ["customer","consultant","date","note"]
site.register(ConsultRecord,ConsultRecordConfig)

class StudentConfig(ModelSatrk):

    def score_show(self,obj=None,is_header=False):
        if is_header:
            return "查看成绩"
        return mark_safe("<a href='/stark/app01/student/score_view/%s'>查看成绩</a>"%obj.pk)

    def score_view(self,request,student_id):
        if request.is_ajax():
            cid=request.GET.get("cid")
            sid=request.GET.get("sid")

            study_record_list=StudyRecord.objects.filter(student=sid,course_record__class_obj_id=cid)

            data=[]

            for study_record in study_record_list:
                data.append(["day%s"%study_record.course_record.day_num,study_record.score])

            print(data)

            from django.http import JsonResponse
            return JsonResponse(data,safe=False)
        else:
            obj=Student.objects.filter(pk=student_id).first()
            class_list=obj.class_list.all()

            return render(request,"score_view.html",{"class_list":class_list,"obj":obj})


    def extra_url(self):

        temp=[]
        temp.append(url("score_view/(\d+)",self.score_view))
        return temp



    list_display = ["username","class_list",score_show]





site.register(Student,StudentConfig)


class CourseRecordConfig(ModelSatrk):

    def check(self,obj=None,is_header=False):
        if is_header:
            return "考勤记录"

        return mark_safe("<a href='/stark/app01/studyrecord/?course_record=%s'>考勤</a>"%obj.pk)

    def score_list(self,request,courserecord_id):
       if request.method=="GET":
           '''
           方式1：
           study_record_list = StudyRecord.objects.filter(course_record_id=courserecord_id)
           score_choices = StudyRecord.score_choices
           return render(request, "score_list.html",{"study_record_list": study_record_list, "score_choices": score_choices})

           '''
           from django import forms
           from django.forms import widgets

           # class ScoreForm(forms.Form):
           #     score=forms.ChoiceField(choices=StudyRecord.score_choices,
           #                             widget=widgets.Select(attrs={"class": "form-control"})
           #                             )
           #     homework_note=forms.CharField(
           #
           #         widget=widgets.Textarea(attrs={"class":"form-control"})
           #     )



           study_record_list = StudyRecord.objects.filter(course_record_id=courserecord_id)

           for study_record in study_record_list:
               ScoreForm = type("ScoreForm", (forms.Form,), {
                   "score_%s"%study_record.pk: forms.ChoiceField(choices=StudyRecord.score_choices,
                                                 widget=widgets.Select(attrs={"class": "form-control"})
                                                 ),
                   "homework_note_%s"%study_record.pk: forms.CharField(
                       widget=widgets.Textarea(attrs={"class":"form-control","rows":3,"cols":8})
                   )

               })
               study_record.form=ScoreForm(initial={"score_%s"%study_record.pk:study_record.score,"homework_note_%s"%study_record.pk:study_record.homework_note})

           return render(request, "score_list.html",{"study_record_list": study_record_list})

       else:
           print(request.POST)

           info={}
           for item ,val in request.POST.items():
               if item=="csrfmiddlewaretoken":
                   continue
               field,pk=item.rsplit("_",1)
               if pk not in info:
                    info[pk]={field:val}
               else:
                   info[pk][field]=val

           for pk,update_data in info.items():
               StudyRecord.objects.filter(pk=pk).update(**update_data)



           return redirect(request.path)

    def extra_url(self):
        temp=[]
        temp.append(url("score_list/(\d+)",self.score_list))
        return temp
    def recordscore(self, obj=None, is_header=False):
        if is_header:
            return "录入成绩"

        return mark_safe("<a href='/stark/app01/courserecord/score_list/%s'>录入成绩</a>"%obj.pk)

    list_display_links = ["class_obj"]

    list_display = ["class_obj","day_num",check,recordscore]

    def patch_init(self,queryset):
        print(queryset)
        for course_record in queryset:

            student_list=Student.objects.filter(class_list=course_record.class_obj)
            for student in student_list:

                StudyRecord.objects.create(course_record=course_record,student=student)




    patch_init.desc = "批量初始化"

    actions = [patch_init]

site.register(CourseRecord,CourseRecordConfig)

class StudyRecordConfig(ModelSatrk):
    def display_record(self, obj=None, is_header=False):
        if is_header:
            return "记录"
        return obj.get_record_display()

    def display_score(self, obj=None, is_header=False):
        if is_header:
            return "成绩"
        return obj.get_score_display()



    list_display = ["student","course_record",display_record,display_score]



    def absense(self,queryset):
        queryset.update(record="noshow")
    def vacate(self,queryset):
        queryset.update(record="vacate")

    vacate.desc="请假"
    absense.desc="缺勤"
    actions = [absense,vacate]




site.register(StudyRecord,StudyRecordConfig)

site.register(CustomerDistrbute)