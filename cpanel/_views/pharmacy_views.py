from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from cpanel.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Q
from cpanel.decorators import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='cpanel:login')
def Pharmacy_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Pharmacy, pharmacy=request.POST.get('lab')):
                return HttpResponseNotFound("This Pharmacy data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False
            medical_institution = get_object_or_none(MedicalInstitutions, institution_id=request.POST.get('institution_id'))
            if not medical_institution:
                # Add User to django
                user = User.objects.create_user(
                    username=request.POST.get('institution_id'),
                    password=request.POST.get('password'),
                    is_staff=True
                )

                # Add user to the group
                group = Group.objects.get(name='Pharmacy')
                group.user_set.add(user)

                medical_institution = MedicalInstitutions.objects.create(
                    institution_id=request.POST.get('institution_id'),
                    institution_name=request.POST.get('institution_name'),
                    user=user
                )

                if request.FILES.get('image'):
                    medical_institution.image = request.FILES.get('image')
                    medical_institution.save()

                for phone in request.POST.getlist('phone'):
                    MedicalInstitutionsPhone.objects.create(
                        institution=medical_institution,
                        phone=phone
                    )

                for address in request.POST.getlist('address'):
                    MedicalInstitutionsAddress.objects.create(
                        institution=medical_institution,
                        address=address
                    )

            else:
                group = Group.objects.get(name='Pharmacy')
                group.user_set.add(medical_institution.user)

            owner = get_object_or_none(Pharmacist, pharmacist_nn=request.POST.get('owner'))
            if not owner:
                return HttpResponseNotFound("This Pharmacist data is not stored")

            Pharmacy.objects.create(
                pharmacy=medical_institution,
                pharmacy_type=request.POST.get('pharmacy_type'),
                owner=owner,
                hide=hide
            )

            return HttpResponse()

    return render(request, 'cpanel/Pharmacy/Pharmacy_add.html')


@login_required(login_url='cpanel:login')
def Pharmacy_edit(request, id):
    institution = get_object_or_404(MedicalInstitutions, institution_id=id)
    institution_numbers = institution.get_phone
    institution_address = institution.get_address
    pharmacy = get_object_or_404(Pharmacy, pharmacy=id)
    # Data Editing
    if request.is_ajax():
        if request.method == "POST":
            # data preprocessing
            hide = True if request.POST.get('hide') == 'on' else False

            # Handle stakeholder
            institution.institution_name = request.POST.get('institution_name')

            # Handle stakeholder image
            if request.FILES.get('image'):
                institution.image = request.FILES.get('image')

            institution.save()

            # Handle password
            if request.POST.get('password'):
                user = get_object_or_none(User, username=institution)
                if user.check_password(request.POST.getlist('password')[0]):
                    user.set_password(request.POST.getlist('password')[1])
                    user.save()

            # Handle phone
            old_numbers = [i.phone for i in institution_numbers]
            for number in request.POST.getlist('phone'):
                if number in old_numbers:
                    old_numbers.remove(number)
                else:
                    MedicalInstitutionsPhone.objects.create(
                        institution=institution,
                        phone=number
                    )
            delete_phones = [i for i in institution_numbers if i.phone in old_numbers]
            for instance in delete_phones:
                instance.delete()

            # Handle address
            old_address = [i.address for i in institution_address]
            for address in request.POST.getlist('address'):
                if address in old_address:
                    old_address.remove(address)
                else:
                    MedicalInstitutionsAddress.objects.create(
                        institution=institution,
                        address=address
                    )
            delete_address = [i for i in institution_address if i.address in old_address]
            for instance in delete_address:
                instance.delete()

            # Pharmacy Handle
            pharmacy.pharmacy_type = request.POST.get('pharmacy_type')
            owner = get_object_or_none(Pharmacist, pharmacist_nn=request.POST.get('owner'))
            if not owner:
                return HttpResponseNotFound("This Pharmacist data is not stored")
            pharmacy.owner = owner
            pharmacy.hide = hide

            pharmacy.save()

            return HttpResponse()

    context = {
        'institution': institution,
        'main_phone': institution_numbers[0].phone,
        'phones': institution_numbers[1:],
        'main_address': institution_address[0].address,
        'address': institution_address[1:],
        'pharmacy': pharmacy,

    }
    return render(request, 'cpanel/Pharmacy/Pharmacy_edit.html', context)


@login_required(login_url='cpanel:login')
@allowed_users(['Admin', 'Pharmacy'])
def Pharmacy_list(request):
    pharmacies = Pharmacy.objects.all().filter(hide=False)
    if request.method == 'POST':
        pharmacy = get_object_or_none(Pharmacy, pharmacy=request.POST.get('id'))
        if pharmacy:
            pharmacy.hide = True
            pharmacy.save()
    context = {
        "pharmacies": pharmacies,
    }
    return render(request, 'cpanel/Pharmacy/Pharmacy_list.html', context)
