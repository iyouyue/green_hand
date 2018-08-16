


def initial_session(request,user):

    # 方式1：
    # permission_info = user.roles.all().values("permissions__url", "permissions__title").distinct()
    # temp = []
    # for i in permission_info:
    #     temp.append(i["permissions__url"])
    # request.session["permission_list"] = temp  # ["url","url1",.....]
    # 方式2：
    # 创建一个数据格式：  包含所有权限url，权限所在组，权限的编号

    permission_info = user.roles.all().values("permissions__id",
                                              "permissions__url",
                                              "permissions__title",
                                              "permissions__permission_group_id",
                                              "permissions__code",
                                              "permissions__parent_id",
                                              "permissions__permission_group__menu__caption",
                                              "permissions__permission_group__menu_id",
                                              ).distinct()

    print("permission_info",permission_info)

    # 创建生成菜单的数据
    permission_list=[]
    # permission_info=[{"permissions__url":"",permissions__title:""},{}]
    for permission_item in permission_info:
        temp={
            "id":permission_item["permissions__id"],
            "url":permission_item["permissions__url"],
            "title":permission_item["permissions__title"],
            "pid":permission_item["permissions__parent_id"],
            "menu_name":permission_item["permissions__permission_group__menu__caption"],
            "menu_id":permission_item["permissions__permission_group__menu_id"],

        }
        permission_list.append(temp)

    request.session["permission_list"]=permission_list

    '''
    将permission_info---->


     menu_dict = {
        1: {
            "title": "菜单一",
            "active": False,
            "children": [
                {"title": "添加用户", "url": "xxxxxxxxxxx", "active": False},
                {"title": "查看用户", "url": "xxxxxxxxxxx", "active": False},

            ]},

        2: {
            "title": "菜单二",
            "active": True,
            "children": [
                {"title": "添加用户", "url": "xxxxxxxxxxx", "active": False},
                {"title": "查看用户", "url": "xxxxxxxxxxx", "active": True},

            ]

        }}


    '''







    # 将登录用户所有权限信息写入到session中
    permission_dict = {}

    for item in permission_info:
        gid = item["permissions__permission_group_id"]
        if gid in permission_dict:

            permission_dict[gid]["urls"].append(item["permissions__url"]),
            permission_dict[gid]["codes"].append(item["permissions__code"]),


        else:
            permission_dict[gid] = {
                "urls": [item["permissions__url"], ],
                "codes": [item["permissions__code"]]

            }
    request.session["permission_dict"]=permission_dict

    '''
    元数据：
    permission_list=[
        {"permissions__url":"/orders/","permissions__group_id":"2","permissions__code":"list"},

    ]
    转换数据：
    permission_dict = {
        2: {
            "urls": ["/orders/","/orders/add","/orders/delete/(\d+)",],
            "codes": ["list","add","delete",]
        },
        1: {
            "urls": ["/users/","xxx" ],
            "codes": ["list","xxx" ]
        },
    }



    '''


    '''
   egon:

   permission_dict={
       2:{
           "urls":["orders",],
           "codes:["list",]
       }

   }

   alex:
   permission_dict=

   {
     1:{
       "urls":["/users/"],
       "codes":["list"]
      },
     2:{
        "urls":["/orders/","/orders/add"],
        "codes":["list","add"]
     }

   }

   request.session["permission_dict"]=permission_dict


   '''







