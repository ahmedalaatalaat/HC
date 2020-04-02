from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from cpanel.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from cpanel.decorators import *
from django.db.models import Q


# @allowed_users(['Stakeholder', 'Lab', 'Clinic', 'Hospital'])
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
                return HttpResponseNotFound("This Patient national number not exists")
            else:
                patient = get_object_or_none(Patient, patient_nn=request.POST.get('patient_nn'))

            if not get_object_or_none(Physician, physician_nn=request.POST.get('physician_nn')):
                return HttpResponseNotFound("This physician national number not exists")
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


def Patient_history_edit(request, id):
    patient_history = get_object_or_404(PatientHistory, id=id)
    if request.is_ajax():
        if request.method == "POST":
            # data preprocessing
            hide = True if request.POST.get('hide') == 'on' else False

            patient_history.date_time = request.POST.get('date_time')
            patient_history.visitation_type = request.POST.get('visitation_type')
            patient_history.prescription = request.POST.get('prescription')
            patient_history.physician_comments = request.POST.get('physician_comments')
            patient_history.diagnouse = request.POST.get('diagnouse')
            patient_history.analysis_radiology = request.POST.get('analysis_radiology')
            patient_history.disease_priority = request.POST.get('disease_priority')
            patient_history.hide = hide

            patient_history.save()

    context = {
        'patient_history': patient_history
    }
    return render(request, 'cpanel/Patient/Patient_History_edit.html', context)


@allowed_users(['Admin', 'Patient'])
def Patient_history_list(request):
    if str(request.user.groups.all().first()) == 'Patient':
        user = user.request
        patients_history = PatientHistory.objects.all().filter(
            Q(hide=False) &
            Q(patient_nn__patient_nn__user=user)).distinct()
    else:
        patients_history = PatientHistory.objects.all().filter(hide=False)
    if request.method == 'POST':
        history = get_object_or_none(PatientHistory, id=request.POST.get('id'))
        if history:
            history.hide = True
            history.save()
    context = {
        "patients_history": patients_history,
    }
    return render(request, 'cpanel/Patient/Patient_History_list.html', context)
