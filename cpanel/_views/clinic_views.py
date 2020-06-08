from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from cpanel.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Q
from cpanel.decorators import *


def Clinic_add(request):
    specializations = Specialization.objects.all()
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Clinic, clinic=request.POST.get('clinic')):
                return HttpResponseNotFound("This Clinic data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False
            ER = True if request.POST.get('er_availability') == 'on' else False

            medical_institution = get_object_or_none(MedicalInstitutions, institution_id=request.POST.get('institution_id'))
            if not medical_institution:
                # Add User to django
                user = User.objects.create_user(
                    username=request.POST.get('institution_id'),
                    password=request.POST.get('password'),
                    is_staff=True
                )

                # Add user to the group
                group = Group.objects.get(name='Clinic')
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
                group = Group.objects.get(name='Clinic')
                group.user_set.add(medical_institution.user)

            clinic = Clinic.objects.create(
                clinic=medical_institution,
                email=request.POST.get('email'),
                fax=request.POST.get('fax'),
                er_availability=ER,
                hide=hide
            )

            for specialization in request.POST.getlist('specialization'):
                specialty = get_object_or_none(Specialization, name=specialization)
                ClinicSpecialization.objects.create(
                    clinic=clinic,
                    specialization=specialty
                )

            return HttpResponse()

    context = {
        'specializations': specializations
    }

    return render(request, 'cpanel/Clinic/Clinic_add.html', context)


def Clinic_edit(request, id):
    specializations = Specialization.objects.all()
    institution = get_object_or_404(MedicalInstitutions, institution_id=id)
    institution_numbers = institution.get_phone
    institution_address = institution.get_address
    clinic = get_object_or_404(Clinic, clinic=id)
    clinic_specializations = [i.specialization for i in clinic.get_Specialization]

    if request.is_ajax():
        if request.method == "POST":
            # data preprocessing
            hide = True if request.POST.get('hide') == 'on' else False
            ER = True if request.POST.get('er_availability') == 'on' else False

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

            # Clinic Handle
            clinic.email = request.POST.get('email')
            clinic.fax = request.POST.get('fax')
            clinic.er_availability = ER
            clinic.hide = hide

            clinic.save()

            # Handle Specialization
            old_specializations = [str(i) for i in clinic_specializations]

            for specialization in request.POST.getlist('specialization'):
                if specialization in old_specializations:
                    old_specializations.remove(specialization)
                else:
                    specialization = get_object_or_none(specializations, name=specialization)
                    ClinicSpecialization.objects.create(
                        clinic=clinic,
                        specialization=specialization
                    )

            delete_specializations = [i for i in clinic_specializations if str(i) in old_specializations]
            for instance in delete_specializations:
                ClinicSpecialization.objects.all().filter(
                    clinic=clinic,
                    specialization=instance
                ).delete()

    context = {
        'institution': institution,
        'main_phone': institution_numbers[0].phone,
        'phones': institution_numbers[1:],
        'main_address': institution_address[0].address,
        'address': institution_address[1:],
        'clinic': clinic,
        'specializations': specializations,
        'clinic_specializations': clinic_specializations

    }

    return render(request, 'cpanel/Clinic/Clinic_edit.html', context)


@allowed_users(['Admin', 'Physician', 'Nurse', 'Specialist', 'Pharmacist', 'Clinic'])
def Clinic_list(request):
    if str(request.user.groups.all().first()) == 'Physician':
        clinics = set()
        user = request.user
        physicianClinic = PhysicianClinicWorkingTime.objects.all().filter(
            Q(hide=False) &
            Q(physician_nn__physician_nn__user=user)).distinct()
        for physicians in physicianClinic:
            clinics.add(physicians.clinic)

    elif str(request.user.groups.all().first()) == 'Specialist':
        clinics = set()
        user = request.user
        clinicSpecialists = ClinicSpecialists.objects.all().filter(
            # Q(hide=False) &
            Q(specialist_nn__specialist_nn__user=user)).distinct()
        for specialists in clinicSpecialists:
            clinics.add(specialists.clinic)

    elif str(request.user.groups.all().first()) == 'Nurse':
        clinics = set()
        user = request.user
        clinicNurses = ClinicNurses.objects.all().filter(
            # Q(hide=False) &
            Q(nurse_nn__nurse_nn__user=user)).distinct()
        for nurses in clinicNurses:
            clinics.add(nurses.clinic)

    else:
        clinics = Clinic.objects.all().filter(hide=False)
    if request.method == 'POST':
        clinic = get_object_or_none(Clinic, clinic=request.POST.get('id'))
        if clinic:
            clinic.hide = True
            clinic.save()

    context = {
        "clinics": clinics,
    }
    return render(request, 'cpanel/Clinic/Clinic_list.html', context)
