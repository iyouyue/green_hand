import requests

# json参数
"""
标志：Form Data

请求头：http://www.oldboyedu.com       headers  ...
请求体：name=alex&age=18
"""
requests.post(
    url='http://www.oldboyedu.com',
    data={
        'name':'alex',
        'age':18
    },
    headers={},
    cookies={}
)
"""
标志：payload ...

请求头：http://www.oldboyedu.com       headers  ...
请求体：'{"name":"alex","age":18}'
"""
requests.post(
    url='http://www.oldboyedu.com',
    json={
        'name':'alex',
        'age':18
    },
    headers={},
    cookies={}
)
# ##################################################################
"""
请求头：http://www.oldboyedu.com       headers  ...
请求体：name=alex&age=18
"""
requests.post(
    url='http://www.oldboyedu.com',
    data={
        'name':'alex',
        'age':18
    },
    headers={},
    cookies={}
)

"""
请求头：http://www.oldboyedu.com       headers  ...
请求体：'{"name":"alex","age":18}'
"""
requests.post(
    url='http://www.oldboyedu.com',
    data=json.dumps({
        'name':'alex',
        'age':18
    }),
    headers={},
    cookies={}
)


