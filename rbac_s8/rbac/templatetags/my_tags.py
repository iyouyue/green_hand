

from django import template

register=template.Library()

@register.simple_tag
def mul(x,y):
    return x*y

@register.inclusion_tag("menu.html")
def get_menu(request):
    permission_list = request.session["permission_list"]

    #############temp_dict:存储所有放到菜单栏中的权限
    temp_dict = {}
    for item in permission_list:
        pid = item["pid"]
        if not pid:
            item["active"] = False
            temp_dict[item["id"]] = item

    # print(temp_dict)


    #######将需要标中的active设置True
    current_path = request.path_info
    import re
    for item in permission_list:
        pid = item["pid"]
        url = "^%s$" % item["url"]
        if re.match(url, current_path):
            if pid:
                temp_dict[pid]["active"] = True
            else:
                item["active"] = True

    ########将temp_dict转换为最终的menu_dict的数据格式

    menu_dict = {}
    for item in temp_dict.values():

        if item["menu_id"] in menu_dict:

            temp = {"title": item["title"], "url": item["url"], "active": item["active"]},
            menu_dict[item["menu_id"]]["children"].append(temp)

            if item["active"]:
                menu_dict[item["menu_id"]]["active"] = True
        else:

            menu_dict[item["menu_id"]] = {

                "title": item["menu_name"],
                "active": item["active"],
                "children": [
                    {"title": item["title"], "url": item["url"], "active": item["active"]},
                ]

            }
    print(menu_dict)

    return {"menu_dict":menu_dict}