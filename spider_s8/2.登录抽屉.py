import requests
from bs4 import BeautifulSoup
# 1. 先访问抽屉新热榜，获取cookie（未授权）
r1 = requests.get(
    url='https://dig.chouti.com/all/hot/recent/1',
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
)
r1_cookie_dict = r1.cookies.get_dict()


# 2. 发送用户名和密码认证 + cookie（未授权）
response_login = requests.post(
    url='https://dig.chouti.com/login',
    data={
        'phone':'8613121758648',
        'password':"woshiniba",
        'oneMonth':'1'
    },
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    },
    cookies=r1_cookie_dict
)

for page_num in range(2,3):

    response_index = requests.get(
        url='https://dig.chouti.com/all/hot/recent/%s' %page_num,
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
    )
    soup = BeautifulSoup(response_index.text,'html.parser')
    div = soup.find(attrs={'id':'content-list'})
    items = div.find_all(attrs={'class':'item'})
    for item in items:
        tag = item.find(attrs={'class':'part2'})
        nid = tag.get('share-linkid')

        # 根据每一个新闻ID点赞
        r1 = requests.post(
            url='https://dig.chouti.com/link/vote?linksId=%s' %nid,
            headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            },
            cookies=r1_cookie_dict
        )
        print(r1.text)