from django.shortcuts import render, get_object_or_404, redirect
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm


def cpanel(request):
    stakeholder = get_object_or_404(Stakeholders, user=request.user)
    context = {
        'stakeholder': stakeholder,
    }
    return render(request, 'cpanel/cpanel.html', context)


# login Views
def loginView(request):
    form = AuthenticationForm()
    error = False
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            group = Group.objects.filter(user=user).first()
            if request.POST.get('login_as') == str(group):
                login(request, user)
                return redirect('cpanel:doctor_add')
            elif (str(group) == 'Clinic' or str(group) == 'Hospital' or str(group) == 'Lab' or str(group) == 'Pharmacy') and request.POST.get('login_as') == 'Medical Institution':
                login(request, user)
                return redirect('cpanel:doctor_add')
            else:
                error = True

    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'cpanel/login.html', context)


def forgot_password(request):
    return render(request, 'cpanel/forgot_password.html')


def lock_screen(request):
    return render(request, 'cpanel/lock_screen.html')


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
