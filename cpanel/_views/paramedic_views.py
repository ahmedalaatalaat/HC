from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from cpanel.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required(login_url='cpanel:login')
def Paramedic_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Paramedic, paramedic_nn=request.POST.get('national_number')):
                return HttpResponseNotFound("This Paramedic data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('national_number'))
            if not stakeholder:
                user = User.objects.create_user(
                    username=request.POST.get('national_number'),
                    password=request.POST.get('password'),
                    is_staff=True
                )

                # Add user to the group
                group = Group.objects.get(name='Paramedic')
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
                group = Group.objects.get(name='Paramedic')
                group.user_set.add(stakeholder.user)

            paramedic = Paramedic.objects.create(
                paramedic_nn=stakeholder,
                ambulance_palte_number=request.POST.get('ambulance_palte_number'),
                hide=hide
            )

            return HttpResponse()

    return render(request, 'cpanel/Paramedic/Paramedic_add.html')


@login_required(login_url='cpanel:login')
def Paramedic_edit(request, NN):
    stakeholder = get_object_or_404(Stakeholders, national_number=NN)
    stakeholder_numbers = stakeholder.get_phone
    stakeholder_address = stakeholder.get_address
    paramedic = get_object_or_404(Paramedic, paramedic_nn=NN)

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

            # Handle paramedic
            paramedic.hide = hide
            paramedic.ambulance_palte_number = request.POST.get('ambulance_palte_number')

            paramedic.save()

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
        'paramedic': paramedic,
    }
    return render(request, 'cpanel/Paramedic/Paramedic_edit.html', context)


@login_required(login_url='cpanel:login')
def Paramedic_list(request):
    paramedics = Paramedic.objects.all().filter(hide=False)
    if request.method == 'POST':
        paramedic = get_object_or_none(Paramedic, paramedic_nn=request.POST.get('id'))
        if paramedic:
            paramedic.hide = True
            paramedic.save()
    context = {
        "paramedics": paramedics,
    }
    return render(request, 'cpanel/Paramedic/Paramedic_list.html', context)
