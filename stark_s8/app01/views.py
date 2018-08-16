from django.shortcuts import render,HttpResponse

# Create your views here.

from .models import Book


def test(request):
    publish=Book._meta.get_field("publish")
    print(publish.rel.to.objects.all())

    authors = Book._meta.get_field("authors")
    print(authors.rel.to.objects.all())

    return HttpResponse("123")