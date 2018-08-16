import requests
from bs4 import BeautifulSoup


r1 = requests.get(
    url='https://github.com/login'
)
s1 = BeautifulSoup(r1.text,'html.parser')
token = s1.find(name='input',attrs={'name':'authenticity_token'}).get('value')
print(token)


r2 = requests.post(
    url='https://github.com/session',
    data={
        'commit':'Sign in',
        'utf8':'✓',
        'authenticity_token':token,
        'login':'xxx',
        'password':'xxxx'
    }
)
