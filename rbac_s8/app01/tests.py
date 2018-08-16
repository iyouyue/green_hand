from django.test import TestCase

# Create your tests here.


import re

ret=re.match("/users/edit/(\d+)","/users/edi23t/3")
print(ret)