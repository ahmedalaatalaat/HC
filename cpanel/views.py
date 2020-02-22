from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Doctor Views
def Doctor_add(request):
    specializations = Specialization.objects.all()
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Physician, physician_nn=request.POST.get('national_number')):
                return HttpResponseNotFound("This doctor data is already stored")

            # data preprocessing
            hide = True if request.POST.get('hide') == 'on' else False
            date = request.POST.get('birthday').split('-')
            date = f'{date[2]}-{date[0]}-{date[1]}'

            stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('national_number'))
            if not stakeholder:
                # Add User to django
                user = User.objects.create_user(
                    username=request.POST.get('national_number'),
                    password=request.POST.get('password')
                )

                # Add user to the group
                group = Group.objects.get(name='Physician')
                group.user_set.add(user)

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
                group = Group.objects.get(name='Physician')
                group.user_set.add(stakeholder.user)

            physician = Physician.objects.create(
                physician_nn=stakeholder,
                title=request.POST.get('title'),
                hide=hide
            )

            for specialization in request.POST.getlist('specialization'):
                specialty = get_object_or_none(Specialization, name=specialization)
                PhysicianSpecialization.objects.create(
                    physician_nn=physician,
                    specialization=specialty
                )

            return HttpResponse()

    context = {
        'specializations': specializations
    }
    return render(request, 'cpanel/Doctor/Doctor_add.html', context)


def Doctor_edit(request, NN):
    # Passed Data
    specializations = Specialization.objects.all()
    stakeholder = get_object_or_404(Stakeholders, national_number=NN)
    stakeholder_numbers = stakeholder.get_phone
    stakeholder_address = stakeholder.get_address
    doctor = get_object_or_404(Physician, physician_nn=NN)
    doctor_specializations = [i.get_value() for i in doctor.get_Specialization]

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
            doctor.hide = hide
            doctor.title = request.POST.get('title')

            doctor.save()

            # Handle Specialization
            old_specializations = doctor_specializations
            for specialization in request.POST.getlist('specialization'):
                if specialization in old_specializations:
                    old_specializations.remove(specialization)
                else:
                    specialization = get_object_or_none(specializations, name=specialization)
                    PhysicianSpecialization.objects.create(
                        physician_nn=doctor,
                        specialization=specialization
                    )

            delete_specializations = [i for i in specializations if i.name in old_specializations]
            for instance in delete_specializations:
                PhysicianSpecialization.objects.all().filter(
                    physician_nn=doctor,
                    specialization=instance
                ).delete()

    context = {
        'stakeholder': stakeholder,
        'main_phone': stakeholder_numbers[0].phone,
        'phones': stakeholder_numbers[1:],
        'main_address': stakeholder_address[0].address,
        'address': stakeholder_address[1:],
        'specializations': specializations,
        'doctor': doctor,
        'doctor_specializations': doctor_specializations,
    }
    return render(request, 'cpanel/Doctor/Doctor_edit.html', context)


def Doctor_list(request):
    doctors = Physician.objects.all().filter(hide=False)
    if request.method == 'POST':
        doctor = get_object_or_none(Physician, physician_nn=request.POST.get('id'))
        if doctor:
            doctor.hide = True
            doctor.save()
    context = {
        "doctors": doctors,
    }
    return render(request, 'cpanel/Doctor/Doctor_list.html', context)


# Patient Views
def Patient_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Patient, patient_nn=request.POST.get('national_number')):
                return HttpResponseNotFound("This Patient data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('national_number'))
            if not stakeholder:
                # Add User to django
                user = User.objects.create_user(
                    username=request.POST.get('national_number'),
                    password=request.POST.get('password')
                )

                # Add user to the group
                group = Group.objects.get(name='Patient')
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

                for address in request.POST.getlist('address'):
                    StakeholdersAddress.objects.create(
                        national_number=stakeholder,
                        address=address
                    )

                for phone in request.POST.getlist('phone'):
                    StakeholdersPhones.objects.create(
                        national_number=stakeholder,
                        phone=phone
                    )
            else:
                group = Group.objects.get(name='Patient')
                group.user_set.add(stakeholder.user)

            patient = Patient.objects.create(
                patient_nn=stakeholder,
                blood_type=request.POST.get('blood_type'),
                chronic_diseases_name=request.POST.get('chronic_diseases_name'),
                chronic_diseases_type=request.POST.get('chronic_diseases_type'),
                hide=hide
            )

            for phone in request.POST.getlist('relatives_phones'):
                PatientRelativesPhones.objects.create(
                    patient_nn=patient,
                    phone=phone
                )

            return HttpResponse()
    return render(request, 'cpanel/Patient/Patient_add.html')


def Patient_edit(request, NN):
    stakeholder = get_object_or_404(Stakeholders, national_number=NN)
    stakeholder_numbers = stakeholder.get_phone
    stakeholder_address = stakeholder.get_address
    patient = get_object_or_404(Patient, patient_nn=NN)
    patient_relatives_phones = patient.get_PatientRelativesPhones

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
                    try:
                        StakeholdersPhones.objects.create(
                            national_number=stakeholder,
                            phone=number
                        )
                    except Exception:
                        pass
            delete_phones = [i for i in stakeholder_numbers if i.phone in old_numbers]
            for instance in delete_phones:
                instance.delete()

            # Handle address
            old_address = [i.address for i in stakeholder_address]
            for address in request.POST.getlist('address'):
                if address in old_address:
                    old_address.remove(address)
                else:
                    try:
                        StakeholdersAddress.objects.create(
                            national_number=stakeholder,
                            address=address
                        )
                    except Exception:
                        pass
            delete_address = [i for i in stakeholder_address if i.address in old_address]
            for instance in delete_address:
                instance.delete()

            # Handle Patient
            patient.blood_type = request.POST.get('blood_type')
            patient.chronic_diseases_name = request.POST.get('chronic_diseases_name')
            patient.chronic_diseases_type = request.POST.get('chronic_diseases_type')
            patient.hide = hide
            patient.save()

            # Handle Patient Relatives Phone
            old_relatives_numbers = [i.phone for i in patient_relatives_phones]
            for number in request.POST.getlist('relatives_phones'):
                if number in old_relatives_numbers:
                    old_relatives_numbers.remove(number)
                else:
                    try:
                        PatientRelativesPhones.objects.create(
                            patient_nn=patient,
                            phone=number
                        )
                    except Exception:
                        pass
            delete_phones = [i for i in patient_relatives_phones if i.phone in old_relatives_numbers]
            for instance in delete_phones:
                instance.delete()

    context = {
        'stakeholder': stakeholder,
        'main_phone': stakeholder_numbers[0].phone,
        'phones': stakeholder_numbers[1:],
        'main_relative_phone': patient_relatives_phones[0].phone,
        'relative_phones': patient_relatives_phones[1:],
        'main_address': stakeholder_address[0].address,
        'address': stakeholder_address[1:],
        'patient': patient,
    }
    return render(request, 'cpanel/Patient/Patient_edit.html', context)


def Patient_list(request):
    patients = Patient.objects.all().filter(hide=False)
    if request.method == 'POST':
        patient = get_object_or_none(Patient, patient_nn=request.POST.get('id'))
        if patient:
            patient.hide = True
            patient.save()
    context = {
        "patients": patients,
    }
    return render(request, 'cpanel/Patient/Patient_list.html', context)


# Patient History Views
def Patient_history_add(request):
    if request.is_ajax():
        if request.method == 'POST':

            hide = True if request.POST.get('hide') == 'on' else False

            if not get_object_or_none(Patient, patient_nn=request.POST.get('patient_nn')):
                return HttpResponseNotFound("This Patient national number not exist")
            else:
                patient = get_object_or_none(Patient, patient_nn=request.POST.get('patient_nn'))

            if not get_object_or_none(Physician, physician_nn=request.POST.get('physician_nn')):
                return HttpResponseNotFound("This physician national number not exist")
            else:
                physician = get_object_or_none(Physician, physician_nn=request.POST.get('physician_nn'))

            patienthistory = PatientHistory.objects.create(
                patient_nn=patient,
                physician_nn=physician,
                date_time=request.POST.get('date_time'),
                visitation_type=request.POST.get('visitation_type'),
                prescription=request.POST.get('prescription'),
                physician_comments=request.POST.get('physician_comments'),
                diagnouse=request.POST.get('diagnouse'),
                analysis_radiology=request.POST.get('analysis_radiology'),
                disease_priority=request.POST.get('disease_priority'),
                hide=hide
            )

            return HttpResponse()
    return render(request, 'cpanel/Patient/Patient_History_add.html')


def Patient_history_edit(request, NN):
    pass


def Patient_history_list(request):
    patients_history = PatientHistory.objects.all()
    context = {
        "patients_history": patients_history,
    }
    return render(request, 'cpanel/Patient/Patient_History_list.html', context)


# Nurse Views
def Nurse_add(request):
    specializations = Specialization.objects.all()
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Nurse, nurse_nn=request.POST.get('national_number')):
                return HttpResponseNotFound("This Nurse data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('national_number'))
            if not stakeholder:
                user = User.objects.create_user(
                    username=request.POST.get('national_number'),
                    password=request.POST.get('password')
                )

                # Add user to the group
                group = Group.objects.get(name='Nurse')
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
                group = Group.objects.get(name='Nurse')
                group.user_set.add(stakeholder.user)

            nurse = Nurse.objects.create(
                nurse_nn=stakeholder,
                hide=hide
            )

            for specialization in request.POST.getlist('specialization'):
                specialty = get_object_or_none(Specialization, name=specialization)
                NurseSpecialization.objects.create(
                    nurse_nn=nurse,
                    specialization=specialty
                )

            return HttpResponse()
    context = {
        'specializations': specializations
    }
    return render(request, 'cpanel/Nurse/Nurse_add.html', context)


def Nurse_edit(request, NN):
    specializations = Specialization.objects.all()
    stakeholder = get_object_or_404(Stakeholders, national_number=NN)
    stakeholder_numbers = stakeholder.get_phone
    stakeholder_address = stakeholder.get_address
    nurse = get_object_or_404(Nurse, nurse_nn=NN)
    nurse_specializations = [i.get_value() for i in nurse.get_Specialization]

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
            nurse.hide = hide

            nurse.save()

            # Handle Specialization
            old_specializations = nurse_specializations
            for specialization in request.POST.getlist('specialization'):
                if specialization in old_specializations:
                    old_specializations.remove(specialization)
                else:
                    specialization = get_object_or_none(specializations, name=specialization)
                    NurseSpecialization.objects.create(
                        nurse_nn=nurse,
                        specialization=specialization
                    )

            delete_specializations = [i for i in specializations if i.name in old_specializations]
            for instance in delete_specializations:
                NurseSpecialization.objects.all().filter(
                    nurse_nn=nurse,
                    specialization=instance
                ).delete()

    context = {
        'stakeholder': stakeholder,
        'main_phone': stakeholder_numbers[0].phone,
        'phones': stakeholder_numbers[1:],
        'main_address': stakeholder_address[0].address,
        'address': stakeholder_address[1:],
        'nurse': nurse,
        'specializations': specializations,
        'nurse_specializations': nurse_specializations
    }
    return render(request, 'cpanel/Nurse/Nurse_edit.html', context)


def Nurse_list(request):
    nurses = Nurse.objects.all().filter(hide=False)
    if request.method == 'POST':
        nurse = get_object_or_none(Nurse, nurse_nn=request.POST.get('id'))
        if nurse:
            nurse.hide = True
            nurse.save()
    context = {
        "nurses": nurses,
    }
    return render(request, 'cpanel/Nurse/Nurse_list.html', context)


# Paramedic Views
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
                    password=request.POST.get('password')
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
    context = {
        'stakeholder': stakeholder,
        'main_phone': stakeholder_numbers[0].phone,
        'phones': stakeholder_numbers[1:],
        'main_address': stakeholder_address[0].address,
        'address': stakeholder_address[1:],
        'paramedic': paramedic,
    }
    return render(request, 'cpanel/Paramedic/Paramedic_edit.html', context)


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


# Paramedic Views
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


# Specialist Views
def Specialist_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Specialist, specialist_nn=request.POST.get('national_number')):
                return HttpResponseNotFound("This Specialist data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('national_number'))
            if not stakeholder:
                user = User.objects.create_user(
                    username=request.POST.get('national_number'),
                    password=request.POST.get('password')
                )

                # Add user to the group
                group = Group.objects.get(name='Specialist')
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
                group = Group.objects.get(name='Specialist')
                group.user_set.add(stakeholder.user)

            specialist = Specialist.objects.create(
                specialist_nn=stakeholder,
                hide=hide
            )

            for specialization in request.POST.getlist('specialization'):
                SpecialistSpecialization.objects.create(
                    specialist_nn=specialist,
                    specialization=specialization
                )

            return HttpResponse()
    return render(request, 'cpanel/Specialist/Specialist_add.html')


def Specialist_edit(request, NN):
    stakeholder = get_object_or_404(Stakeholders, national_number=NN)
    stakeholder_numbers = stakeholder.get_phone
    stakeholder_address = stakeholder.get_address
    specialist = get_object_or_404(Specialist, specialist_nn=NN)
    specialist_specialization = [i.get_value() for i in specialist.get_Specialization]

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

            # Handle Specialist
            specialist.hide = hide

            specialist.save()

            # Handle Specializations
            old_specializations = [i for i in specialist_specialization]
            for specialization in request.POST.getlist('specialization'):
                if specialization in old_specializations:
                    old_specializations.remove(specialization)
                else:
                    SpecialistSpecialization.objects.create(
                        specialist_nn=specialist,
                        specialization=specialization
                    )
            # delete_specialization = old_specializations
            delete_specialization = [i for i in specialist.get_Specialization if i.get_value() in old_specializations]
            for instance in delete_specialization:
                instance.delete()

    context = {
        'stakeholder': stakeholder,
        'main_phone': stakeholder_numbers[0].phone,
        'phones': stakeholder_numbers[1:],
        'main_address': stakeholder_address[0].address,
        'address': stakeholder_address[1:],
        'main_specialization': specialist_specialization[0],
        'specializations': specialist_specialization[1:],
        'specialist': specialist,
    }
    return render(request, 'cpanel/Specialist/Specialist_edit.html', context)


def Specialist_list(request):
    specialists = Specialist.objects.all().filter(hide=False)
    if request.method == 'POST':
        specialist = get_object_or_none(Specialist, specialist_nn=request.POST.get('id'))
        if specialist:
            specialist.hide = True
            specialist.save()
    context = {
        "specialists": specialists,
    }
    return render(request, 'cpanel/Specialist/Specialist_list.html', context)


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
    pass


def Specialization_list(request):
    specializations = Specialization.objects.all()
    context = {
        "specializations": specializations,
    }
    return render(request, 'cpanel/Specializations/Specialization_list.html', context)


# Stakeholder Views
def Stakeholder_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Stakeholders, national_number=request.POST.get('national_number')):
                return HttpResponseNotFound("This Stakeholder data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('national_number'))
            if not stakeholder:
                # Add User to django
                user = User.objects.create_user(
                    username=request.POST.get('national_number'),
                    password=request.POST.get('password')
                )

                # Add user to the group
                group = Group.objects.get(name='Stakeholder')
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
                    stakeholder_type=request.POST.get('stakeholder_type'),
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
                group = Group.objects.get(name='Stakeholder')
                group.user_set.add(stakeholder.user)

            return HttpResponse()
    return render(request, 'cpanel/Stakeholders/Stakeholders_add.html')


def Stakeholder_edit(request, NN):
    stakeholder = get_object_or_404(Stakeholders, national_number=NN)
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

    context = {
        'stakeholder': stakeholder,
        'main_phone': stakeholder_numbers[0].phone,
        'phones': stakeholder_numbers[1:],
        'main_address': stakeholder_address[0].address,
        'address': stakeholder_address[1:],
    }
    return render(request, 'cpanel/Stakeholders/Stakeholders_edit.html', context)


def Stakeholder_list(request):
    stakeholders = Stakeholders.objects.all().filter(hide=False)
    if request.method == 'POST':
        stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('id'))
        if stakeholder:
            stakeholder.hide = True
            stakeholder.save()

    context = {
        "stakeholders": stakeholders,
    }
    return render(request, 'cpanel/Stakeholders/Stakeholders_list.html', context)


# Clinic Views
def Clinic_add(request):
    specializations = Specialization.objects.all()
    print(request.POST)
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
                    password=request.POST.get('password')
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
    pass


def Clinic_list(request):
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


# Pharmacy Views
def Pharmacy_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Pharmacy, pharmacy=request.POST.get('lab')):
                return HttpResponseNotFound("This Pharmacy data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            Medical_Institutions = MedicalInstitutions.objects.create(
                institution_id=request.POST.get('institution_id'),
                image=request.FILES.get('image'),
                institution_name=request.POST.get('institution_name'),
                hide=hide,
            )

            for phone in request.POST.getlist('phone'):
                MedicalInstitutionsphone.objects.create(
                    institution=Medical_Institutions,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                MedicalInstitutionsAddress.objects.create(
                    institution=Medical_Institutions,
                    address=address
                )

            owner = get_object_or_none(Pharmacist, pharmacist_nn=request.POST.get('owner'))
            if not owner:
                return HttpResponseNotFound("This Pharmacist data is not stored")

            Pharmacy.objects.create(
                pharmacy=request.POST.get('pharmacy'),
                pharmacy_type=request.POST.get('pharmacy_type'),
                owner=owner,
                hide=hide,
            )

            return HttpResponse()

    return render(request, 'cpanel/Pharmacy/Pharmacy_add.html')


def Pharmacy_edit(request, id):
    pass


def Pharmacy_list(request):
    pharmacies = Pharmacy.objects.all()
    context = {
        "pharmacies": pharmacies,
    }
    return render(request, 'cpanel/Pharmacy/Pharmacy_list.html', context)


# Lab Views
def Lab_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Labs, lab=request.POST.get('lab')):
                return HttpResponseNotFound("This lab data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            medical_institution = get_object_or_none(MedicalInstitutions, institution_id=request.POST.get('institution_id'))
            if not medical_institution:
                # Add User to django
                user = User.objects.create_user(
                    username=request.POST.get('institution_id'),
                    password=request.POST.get('password')
                )

                # Add user to the group
                group = Group.objects.get(name='Lab')
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
                group = Group.objects.get(name='Lab')
                group.user_set.add(medical_institution.user)

            lab = Labs.objects.create(
                lab=medical_institution,
                email=request.POST.get('email'),
                fax=request.POST.get('fax'),
                hide=hide
            )

            for analysis in request.POST.getlist('analysis_and_radiology'):
                LabsAnalysisAndRadiology.objects.create(
                    lab=lab,
                    analysis_and_radiology=analysis
                )

            return HttpResponse()

    return render(request, 'cpanel/Lab/Labs_add.html')


def Lab_edit(request, id):
    institution = get_object_or_404(MedicalInstitutions, institution_id=id)
    institution_numbers = institution.get_phone
    institution_address = institution.get_address
    lab = get_object_or_404(Labs, lab=id)
    analysis_and_radiologies = lab.get_analysis_radiology

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

            # lab Handle
            lab.email = request.POST.get('email')
            lab.fax = request.POST.get('fax')
            lab.hide = hide

            lab.save()

            # Handle Analysis And Radiologies
            old_analysis_and_radiologies = [i.analysis_and_radiology for i in analysis_and_radiologies]
            for analysis in request.POST.getlist('analysis_and_radiology'):
                if analysis in old_analysis_and_radiologies:
                    old_analysis_and_radiologies.remove(analysis)
                else:
                    LabsAnalysisAndRadiology.objects.create(
                        lab=lab,
                        analysis_and_radiology=analysis
                    )
            delete_analysis_and_radiologies = [i for i in analysis_and_radiologies if i.analysis_and_radiology in old_analysis_and_radiologies]
            for instance in delete_analysis_and_radiologies:
                instance.delete()

    context = {
        'institution': institution,
        'main_phone': institution_numbers[0].phone,
        'phones': institution_numbers[1:],
        'main_address': institution_address[0].address,
        'address': institution_address[1:],
        'Lab': lab,
        'main_analysis_and_radiologies': analysis_and_radiologies[0].analysis_and_radiology,
        'analysis_and_radiologies': analysis_and_radiologies[1:]
    }

    return render(request, 'cpanel/Lab/Labs_edit.html', context)


def Lab_list(request):
    labs = Labs.objects.all().filter(hide=False)
    if request.method == 'POST':
        lab = get_object_or_none(Labs, lab=request.POST.get('id'))
        if lab:
            lab.hide = True
            lab.save()
    context = {
        "labs": labs,
    }
    return render(request, 'cpanel/Lab/Lab_list.html', context)


# Medical Institution Views
def Medical_Institution_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(MedicalInstitutions, institution_id=request.POST.get('institution_id')):
                return HttpResponseNotFound("This Medical Institutions data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            medical_institution = get_object_or_none(MedicalInstitutions, institution_id=request.POST.get('institution_id'))
            if not medical_institution:
                # Add User to django
                user = User.objects.create_user(
                    username=request.POST.get('institution_id'),
                    password=request.POST.get('password')
                )

                # Add user to the group
                group = Group.objects.get(name='Medical Institution')
                group.user_set.add(user)

                medical_institution = MedicalInstitutions.objects.create(
                    institution_id=request.POST.get('institution_id'),
                    institution_name=request.POST.get('institution_name'),
                    hide=hide,
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
                group = Group.objects.get(name='Medical Institution')
                group.user_set.add(medical_institution.user)

            return HttpResponse()

    return render(request, 'cpanel/Medical Institutions/Medical_institution_add.html')


def Medical_Institution_edit(request, id):
    institution = get_object_or_404(MedicalInstitutions, institution_id=id)
    institution_numbers = institution.get_phone
    institution_address = institution.get_address

    if request.is_ajax():
        if request.method == "POST":
            # data preprocessing
            hide = True if request.POST.get('hide') == 'on' else False

            # Handle stakeholder
            institution.institution_name = request.POST.get('institution_name')
            institution.hide = hide

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

    context = {
        'institution': institution,
        'main_phone': institution_numbers[0].phone,
        'phones': institution_numbers[1:],
        'main_address': institution_address[0].address,
        'address': institution_address[1:],
    }

    return render(request, 'cpanel/Medical Institutions/Medical_institution_edit.html', context)


def Medical_Institution_list(request):
    medical_institutions = MedicalInstitutions.objects.all().filter(hide=False)
    if request.method == 'POST':
        institution = get_object_or_none(MedicalInstitutions, institution_id=request.POST.get('id'))
        if institution:
            institution.hide = True
            institution.save()

    context = {
        "medical_institutions": medical_institutions,
    }
    return render(request, 'cpanel/Medical Institutions/Medical_institution_list.html', context)


# Physician Clinic Working Time Views
def Physician_Clinic_Working_Time_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            physician = get_object_or_none(Physician, physician_nn=request.POST.get('physician_nn'))
            if not physician:
                return HttpResponseNotFound("This doctor data is not stored")

            clinic = get_object_or_none(Clinic, clinic=request.POST.get('clinic'))
            if not clinic:
                return HttpResponseNotFound("This clinic data is not stored")

            for day in request.POST.getlist('week_day'):
                work_day = PhysicianClinicWorkingTime.objects.filter(
                    physician_nn=physician,
                    clinic=clinic,
                    week_day=day,
                    start_time=request.POST.get('start_time'),
                    end_time=request.POST.get('end_time')
                )
                if work_day.count():
                    return HttpResponseNotFound("This working day data is already stored you can go to working days edit")

            hide = True if request.POST.get('hide') == 'on' else False

            for day in request.POST.getlist('week_day'):
                PhysicianClinicWorkingTime.objects.create(
                    physician_nn=physician,
                    clinic=clinic,
                    week_day=day,
                    start_time=request.POST.get('start_time'),
                    end_time=request.POST.get('end_time'),
                    fee=request.POST.get('fee'),
                    hide=hide,
                )
            return HttpResponse()

    return render(request, 'cpanel/Clinic/Physician_Clinic_working_time_add.html')


def Physician_Clinic_Working_Time_edit(request):
    pass


def Physician_Clinic_Working_Time_list(request):
    physician_clinic_working_times = PhysicianClinicWorkingTime.objects.all()
    context = {
        "physician_clinic_working_times": physician_clinic_working_times,
    }
    return render(request, 'cpanel/Clinic/Physician_Clinic_working_time_list.html', context)


# Hospital Views
def Hospital_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Hospital, hospital=request.POST.get('hospital')):
                return HttpResponseNotFound("This hospital data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False
            ER = True if request.POST.get('er_availability') == 'on' else False

            Medical_Institutions = MedicalInstitutions.objects.create(
                institution_id=request.POST.get('institution_id'),
                image=request.FILES.get('image'),
                institution_name=request.POST.get('institution_name'),
                hide=hide,
            )

            for phone in request.POST.getlist('phone'):
                MedicalInstitutionsphone.objects.create(
                    institution=Medical_Institutions,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                MedicalInstitutionsAddress.objects.create(
                    institution=Medical_Institutions,
                    address=address
                )

            Hospital.objects.create(
                hospital=request.POST.get('hospital'),
                email=request.POST.get('email'),
                fax=request.POST.get('fax'),
                er_availability=ER,
                hospital_type=request.POST.get('hospital_type'),
                manager=request.POST.get('manager'),
                hide=hide,
            )

            return HttpResponse()

    return render(request, 'cpanel/Hospital/Hospital_add.html')


def Hospital_edit(request, id):
    pass


def Hospital_list(request):
    hospitals = Hospital.objects.all()
    context = {
        "hospitals": hospitals,
    }
    return render(request, 'cpanel/Hospital/Hospital_list.html', context)


# Physician Hospital Working Time Views
def Physician_Hospital_Working_Time_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            physician = get_object_or_none(Physician, physician_nn=request.POST.get('physician_nn'))
            if not physician:
                return HttpResponseNotFound("This doctor data is not stored")

            hospital = get_object_or_none(Hospital, hospital=request.POST.get('hospital'))
            if not hospital:
                return HttpResponseNotFound("This hospital data is not stored")

            for day in request.POST.getlist('week_day'):
                work_day = PhysicianHospitalWorkingTime.objects.filter(
                    physician_nn=physician,
                    hospital=hospital,
                    week_day=day,
                    start_time=request.POST.get('start_time'),
                    end_time=request.POST.get('end_time')
                )
                if work_day.count():
                    return HttpResponseNotFound("This working day data is already stored you can go to working days edit")

            hide = True if request.POST.get('hide') == 'on' else False

            for day in request.POST.getlist('week_day'):
                PhysicianHospitalWorkingTime.objects.create(
                    physician_nn=physician,
                    hospital=hospital,
                    week_day=day,
                    start_time=request.POST.get('start_time'),
                    end_time=request.POST.get('end_time'),
                    fee=request.POST.get('fee'),
                    hide=hide,
                )
            return HttpResponse()
    return render(request, 'cpanel/Hospital/Physician_Hospital_working_time_add.html')


def Physician_Hospital_Working_Time_edit(request):
    pass


def Physician_Hospital_Working_Time_list(request):
    physician_hospital_working_times = PhysicianHospitalWorkingTime.objects.all()
    context = {
        "physician_hospital_working_times": physician_hospital_working_times,
    }
    return render(request, 'cpanel/Hospital/Physician_Hospital_working_time_list.html', context)


# Insurance Company Views
def Insurance_Company_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(InsuranceCompanies, company_id=request.POST.get('company_id')):
                return HttpResponseNotFound("This Insurance Company data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            company = InsuranceCompanies.objects.create(
                company_id=request.POST.get('company_id'),
                email=request.POST.get('email'),
                fax=request.POST.get('fax'),
                company_name=request.POST.get('company_name'),
                company_type=request.POST.get('company_type'),
                hide=hide
            )

            for phone in request.POST.getlist('phone'):
                InsuranceCompaniesphone.objects.create(
                    company=company,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                InsuranceCompaniesAddress.objects.create(
                    company=company,
                    address=address
                )

            return HttpResponse()
    return render(request, 'cpanel/Insurance Company/Insurance_Company_add.html')


def Insurance_Company_edit(request, id):
    pass


def Insurance_Company_list(request):
    insurance_companies = InsuranceCompanies.objects.all()
    context = {
        "insurance_companies": insurance_companies,
    }
    return render(request, 'cpanel/Insurance Company/Insurance_Company_list.html', context)


# Insurance Type Views
def Insurance_Type_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            company = get_object_or_none(InsuranceCompanies, company_id=request.POST.get('company'))
            if not company:
                return HttpResponseNotFound("This Insurance Company data is not stored")

            if InsuranceTypes.objects.filter(company=company, type_name=request.POST.get('type_name')).count():
                return HttpResponseNotFound("This Insurance Type data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False
            InsuranceTypes.objects.create(
                company=company,
                type_name=request.POST.get('type_name'),
                hide=hide
            )
            return HttpResponse()

    return render(request, 'cpanel/Insurance Company/Insurance_Type_add.html')


def Insurance_Type_edit(request, id):
    pass


def Insurance_Type_list(request):
    insurance_types = InsuranceTypes.objects.all()
    context = {
        "insurance_types": insurance_types,
    }
    return render(request, 'cpanel/Insurance Company/Insurance_Type_list.html', context)
