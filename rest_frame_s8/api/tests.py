from django.test import TestCase

# Create your tests here.
X=12

class C(object):
    def pri(self):
        print(self.x)
class B(C):
    x = X

class Book(B):
    pass
class Publish(B):
    pass

book=Book()
book.pri()

publish=Publish()
publish.pri()