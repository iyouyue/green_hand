from django.test import TestCase

# Create your tests here.



Person=type("Person",(object,),{
    "x":54
})

p2=Person()
print(p2)