from django.db import models

# Create your models here.



class Book(models.Model): # "book"
    title=models.CharField(verbose_name="标题",max_length=32)
    price=models.DecimalField(verbose_name="价格",decimal_places=2,max_digits=5,default=12) # 999.99  1000
    state=models.IntegerField(choices=((1,"已出版"),(2,"未出版")) ,default=1)

    publish=models.ForeignKey(verbose_name="出版社",to="Publish",default=1)
    authors=models.ManyToManyField(to='author',default=1)
    def __str__(self):
        return self.title


class Publish(models.Model):
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name

class author(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()

    def __str__(self):
        return self.name