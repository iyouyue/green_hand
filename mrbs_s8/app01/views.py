from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

from .models import *
import datetime
import json
from django.contrib import auth



def index(request):
    time_choices=Book.time_choices
    room_list=Room.objects.all()

    choice_date = request.GET.get('book_date',datetime.datetime.now().date())
    if isinstance(choice_date,str):
        choice_date = datetime.datetime.strptime(choice_date, '%Y-%m-%d').date()
    book_list=Book.objects.filter(date=choice_date)


    html=""

    for room in room_list:
        s='<tr><td>{0}</td>'.format(room.caption)
        for item in time_choices: #  ((1,"8:00"),())
            flag = False
            for book in book_list:
                if book.room.pk==room.pk and book.time_id==item[0]:
                    flag=True
                    break

            if flag:
                if request.user.pk==book.user.pk:
                    temp = '<td class="active" room_id={0} time_id={1}>{2}</td>'.format(room.pk, item[0],book.user.username)
                else:
                    temp = '<td class="active_other" room_id={0} time_id={1}>{2}</td>'.format(room.pk, item[0],book.user.username)


            else:
                temp = '<td class="item" room_id={0} time_id={1}></td>'.format(room.pk, item[0])

            s+=temp

        s+="</tr>"

        html+=s

    return render(request,"index.html",locals())



def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user = auth.authenticate(username=user, password=pwd)
        if user:
            auth.login(request, user)
            return redirect("/index/")

    return render(request, "login.html")



def book(request):
    choice_date = request.POST.get('date')
    choice_date = datetime.datetime.strptime(choice_date, '%Y-%m-%d').date()
    post_data = json.loads(request.POST.get('data'))
    print(post_data['ADD'])
    response = {'status': True, 'msg': None, 'data': None}
    try:
        # 增加预定     # {"2":["1","2"],"3":["1","2","3"]}
        book_obj_list = []
        for room_id, time_list in post_data['ADD'].items():
            for time_id in time_list:
                obj = Book(room_id=room_id, time_id=time_id, user_id=request.user.pk, date=choice_date)
                book_obj_list.append(obj)
        Book.objects.bulk_create(book_obj_list)

    except Exception as e:
        response['status'] = False
        response['msg'] = str(e)



    from django.http import JsonResponse
    return JsonResponse(response)
