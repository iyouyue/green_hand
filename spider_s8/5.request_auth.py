from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import requests

ret = requests.get('https://api.github.com/user', auth=HTTPBasicAuth('wupeiqi', 'sdfasdfasdf'))
# ret = requests.get('https://api.github.com/user', auth=HTTPDigestAuth('wupeiqi', 'sdfasdfasdf'))
print(ret.text)