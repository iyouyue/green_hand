import requests
from bs4 import BeautifulSoup
# r1 = requests.post(
#     url='https://dig.chouti.com/link/vote?linksId=19319731',
#     headers={
#         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
#     },
#     cookies={
#         'gpsd':'3e2887aa2bba44518c710e4181ba59bb',
#         'gpid':'db9a1305c6b043b1866bd1fd69972f2f'
#     }
# )
# print(r1.text)

response_index = requests.get(
    url='https://dig.chouti.com/',
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
    print(nid)