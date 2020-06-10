from django.shortcuts import render, get_object_or_404, redirect
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='cpanel:login')
def cpanel(request):
    stakeholder = get_object_or_404(Stakeholders, user=request.user)
    context = {
        'stakeholder': stakeholder,
    }
    return render(request, 'cpanel/cpanel.html', context)


@login_required(login_url='cpanel:login')
def user_profile(request):
    stakeholder = get_object_or_404(Stakeholders, user=request.user)
    stakeholder_numbers = stakeholder.get_phone
    stakeholder_address = stakeholder.get_address
    # Data Editing
    if request.is_ajax():
        if request.method == "POST":
            # data preprocessing
            hide = True if request.POST.get('hide') == 'on' else False
            date = request.POST.get('birthday').split('-')
            date = f'{date[2]}-{date[0]}-{date[1]}'

            # Handle stakeholder
            stakeholder.stakeholder_name = request.POST.get('stakeholder_name')
            stakeholder.stakeholder_last_name = request.POST.get('stakeholder_last_name')
            stakeholder.birthday = date
            stakeholder.gender = request.POST.get('gender')
            stakeholder.email = request.POST.get('email')
            stakeholder.marital_status = request.POST.get('marital_status')
            stakeholder.nationality = request.POST.get('nationality')
            stakeholder.cv = request.POST.get('cv')
            stakeholder.stakeholder_type = request.POST.get('stakeholder_type')
            stakeholder.hide = hide

            # Handle stakeholder image
            if request.FILES.get('image'):
                stakeholder.image = request.FILES.get('image')

            stakeholder.save()

            # Handle password
            if request.POST.get('password'):
                user = get_object_or_none(User, username=stakeholder)
                if user.check_password(request.POST.getlist('password')[0]):
                    user.set_password(request.POST.getlist('password')[1])
                    user.save()

            # Handle phone
            old_numbers = [i.phone for i in stakeholder_numbers]
            for number in request.POST.getlist('phone'):
                if number in old_numbers:
                    old_numbers.remove(number)
                else:
                    StakeholdersPhones.objects.create(
                        national_number=stakeholder,
                        phone=number
                    )
            delete_phones = [i for i in stakeholder_numbers if i.phone in old_numbers]
            for instance in delete_phones:
                instance.delete()

            # Handle address
            old_address = [i.address for i in stakeholder_address]
            for address in request.POST.getlist('address'):
                if address in old_address:
                    old_address.remove(address)
                else:
                    StakeholdersAddress.objects.create(
                        national_number=stakeholder,
                        address=address
                    )
            delete_address = [i for i in stakeholder_address if i.address in old_address]
            for instance in delete_address:
                instance.delete()

    try:
        phone = stakeholder_numbers[0].phone
    except Exception:
        phone = None

    try:
        address = stakeholder_address[0].address
    except Exception:
        address = None

    context = {
        'stakeholder': stakeholder,
        'main_phone': phone,
        'phones': stakeholder_numbers[1:],
        'main_address': address,
        'address': stakeholder_address[1:],
    }
    return render(request, 'cpanel/Other/user_profile.html', context)


# login Views
def loginView(request):
    if request.user.is_authenticated:
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('cpanel:home')

    form = AuthenticationForm()
    error = False
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('cpanel:home')
        else:
            error = True

    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'cpanel/Other/login.html', context)


def logoutView(request):
    logout(request)
    return redirect('cpanel:login')


def forgot_password(request):
    return render(request, 'cpanel/forgot_password.html')


def lock_screen(request):
    return render(request, 'cpanel/lock_screen.html')


# Specialization Views
@login_required(login_url='cpanel:login')
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


@login_required(login_url='cpanel:login')
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


@login_required(login_url='cpanel:login')
def Specialization_list(request):
    specializations = Specialization.objects.all()
    context = {
        "specializations": specializations,
    }
    return render(request, 'cpanel/Specializations/Specialization_list.html', context)


def error(request):
    return render(request, 'cpanel/Error/page-404.html')


def error_400(request, exception):
    return render(request, 'cpanel/Error/page-400.html')


def error_403(request, exception):
    return render(request, 'cpanel/Error/page-403.html')


def error_404(request, exception):
    return render(request, 'cpanel/Error/page-404.html')


def error_500(request):
    return render(request, 'cpanel/Error/page-500.html')
