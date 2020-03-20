from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from cpanel.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def Pharmacist_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Pharmacist, pharmacist_nn=request.POST.get('national_number')):
                return HttpResponseNotFound("This Pharmacist data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('national_number'))
            if not stakeholder:
                user = User.objects.create_user(
                    username=request.POST.get('national_number'),
                    password=request.POST.get('password')
                )

                # Add user to the group
                group = Group.objects.get(name='Pharmacist')
                group.user_set.add(user)

                date = request.POST.get('birthday').split('-')
                date = f'{date[2]}-{date[0]}-{date[1]}'
                stakeholder = Stakeholders.objects.create(
                    stakeholder_name=request.POST.get('stakeholder_name'),
                    national_number=request.POST.get('national_number'),
                    stakeholder_last_name=request.POST.get('stakeholder_last_name'),
                    birthday=date,
                    gender=request.POST.get('gender'),
                    email=request.POST.get('email'),
                    marital_status=request.POST.get('marital_status'),
                    nationality=request.POST.get('nationality'),
                    cv=request.POST.get('cv'),
                    user=user
                )

                if request.FILES.get('image'):
                    stakeholder.image = request.FILES.get('image')
                    stakeholder.save()

                for phone in request.POST.getlist('phone'):
                    StakeholdersPhones.objects.create(
                        national_number=stakeholder,
                        phone=phone
                    )

                for address in request.POST.getlist('address'):
                    StakeholdersAddress.objects.create(
                        national_number=stakeholder,
                        address=address
                    )

            else:
                group = Group.objects.get(name='Pharmacist')
                group.user_set.add(stakeholder.user)

            pharmacist = Pharmacist.objects.create(
                pharmacist_nn=stakeholder,
                hide=hide
            )

            for specialization in request.POST.getlist('pharmacist_specialization'):
                PharmacistSpecialization.objects.create(
                    pharmacist_nn=pharmacist,
                    specialization=specialization
                )

            return HttpResponse()
    return render(request, 'cpanel/Pharmacist/Pharmacist_add.html')


def Pharmacist_edit(request, NN):
    stakeholder = get_object_or_404(Stakeholders, national_number=NN)
    stakeholder_numbers = stakeholder.get_phone
    stakeholder_address = stakeholder.get_address
    pharmacist = get_object_or_404(Pharmacist, pharmacist_nn=NN)
    pharmacist_specialization = [i.get_value() for i in pharmacist.get_Specialization]

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

            # Handle Doctor
            pharmacist.hide = hide

            pharmacist.save()

            # Handle Specializations
            old_specializations = pharmacist_specialization
            for specialization in request.POST.getlist('pharmacist_specialization'):
                if specialization in old_specializations:
                    old_specializations.remove(specialization)
                else:
                    PharmacistSpecialization.objects.create(
                        pharmacist_nn=pharmacist,
                        specialization=specialization
                    )
            delete_specialization = old_specializations
            delete_specialization = [i for i in pharmacist.get_Specialization if i.get_value() in old_specializations]
            for instance in delete_specialization:
                instance.delete()

    context = {
        'stakeholder': stakeholder,
        'main_phone': stakeholder_numbers[0].phone,
        'phones': stakeholder_numbers[1:],
        'main_address': stakeholder_address[0].address,
        'address': stakeholder_address[1:],
        'pharmacist': pharmacist,
        'pharmacist_specialization': pharmacist_specialization
    }
    return render(request, 'cpanel/Pharmacist/Pharmacist_edit.html', context)


def Pharmacist_list(request):
    pharmacists = Pharmacist.objects.all().filter(hide=False)
    if request.method == 'POST':
        pharmacist = get_object_or_none(Pharmacist, pharmacist_nn=request.POST.get('id'))
        if pharmacist:
            pharmacist.hide = True
            pharmacist.save()
    context = {
        "pharmacists": pharmacists,
    }
    return render(request, 'cpanel/Pharmacist/Pharmacist_list.html', context)
