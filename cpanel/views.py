from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Specialization Views
def Specialization_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Specialization, specialization_id=request.POST.get('specialization_id')):
                return HttpResponseNotFound("This Specialization data is already stored")
            hide = True if request.POST.get('hide') == 'on' else False
            Specialization.objects.create(
                specialization_id=request.POST.get('specialization_id'),
                name=request.POST.get('name'),
                hide=hide
            )
            return HttpResponse()
    return render(request, 'cpanel/Specializations/Specialization_add.html')


def Specialization_edit(request, id):
    specialization = get_object_or_404(Specialization, specialization_id=id)
    if request.is_ajax():
        if request.method == "POST":
            # data preprocessing
            hide = True if request.POST.get('hide') == 'on' else False

            specialization.name = request.POST.get('name')
            specialization.hide = hide

            specialization.save()

    context = {
        "specialization": specialization,
    }
    return render(request, 'cpanel/Specializations/Specialization_edit.html', context)


def Specialization_list(request):
    specializations = Specialization.objects.all()
    context = {
        "specializations": specializations,
    }
    return render(request, 'cpanel/Specializations/Specialization_list.html', context)
