from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def base(request):
    return render(request, "website/base.html")


def Index(request):
    return render(request, "website/index.html")
    # return HttpResponse("<H1>Home Page</H1>")
