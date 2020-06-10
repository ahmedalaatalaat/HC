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
                    password=request.POST.get('password'),
                    is_staff=True
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


@login_required(login_url='cpanel:login')
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
        'specializations': specializations,
        'doctor': doctor,
        'doctor_specializations': doctor_specializations,
    }
    return render(request, 'cpanel/Doctor/Doctor_edit.html', context)


@login_required(login_url='cpanel:login')
@allowed_users(['Admin', 'Patient'])
def Doctor_list(request):
    if str(request.user.groups.all().first()) == 'Patient':
        doctors = set()
        user = request.user
        patient_history = PatientHistory.objects.all().filter(
            Q(hide=False) &
            Q(patient_nn__patient_nn__user=user)).distinct()
        for history in patient_history:
            doctors.add(history.physician_nn)
    else:
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


@login_required(login_url='cpanel:login')
def Physician_Clinic_Working_Time_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            physician = get_object_or_none(Physician, physician_nn=request.POST.get('physician_nn'))
            if not physician:
                return HttpResponseNotFound("This Doctor national number not exists")

            clinic = get_object_or_none(Clinic, clinic=request.POST.get('clinic'))
            if not clinic:
                return HttpResponseNotFound("This Clinic ID number not exists")

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


@login_required(login_url='cpanel:login')
def Physician_Clinic_Working_Time_edit(request, id):
    work_time = get_object_or_404(PhysicianClinicWorkingTime, id=id)
    if request.is_ajax():
        if request.method == 'POST':
            # print(request.POST)
            hide = True if request.POST.get('hide') == 'on' else False

            work_time.start_time = request.POST.get('start_time')
            work_time.end_time = request.POST.get('end_time')
            print(work_time.end_time)
            work_time.fee = request.POST.get('fee')
            work_time.hide = hide

            work_time.save()

    context = {
        'work_time': work_time
    }
    return render(request, 'cpanel/Clinic/Physician_Clinic_working_time_edit.html', context)


@login_required(login_url='cpanel:login')
def Physician_Clinic_Working_Time_list(request):
    physician_clinic_working_times = PhysicianClinicWorkingTime.objects.all().filter(hide=False)
    if request.method == 'POST':
        work_time = get_object_or_none(PhysicianClinicWorkingTime, id=request.POST.get('id'))
        if work_time:
            work_time.hide = True
            work_time.save()
    context = {
        "physician_clinic_working_times": physician_clinic_working_times,
    }
    return render(request, 'cpanel/Clinic/Physician_Clinic_working_time_list.html', context)


@login_required(login_url='cpanel:login')
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


# Physician Hospital Working Time Views
@login_required(login_url='cpanel:login')
def Physician_Hospital_Working_Time_edit(request, id):
    work_time = get_object_or_404(PhysicianHospitalWorkingTime, id=id)
    if request.is_ajax():
        if request.method == 'POST':
            hide = True if request.POST.get('hide') == 'on' else False

            work_time.start_time = request.POST.get('start_time')
            work_time.end_time = request.POST.get('end_time')
            work_time.fee = request.POST.get('fee')
            work_time.hide = hide

            work_time.save()

    context = {
        'work_time': work_time
    }
    return render(request, 'cpanel/Hospital/Physician_Hospital_working_time_edit.html', context)


@login_required(login_url='cpanel:login')
def Physician_Hospital_Working_Time_list(request):
    physician_hospital_working_times = PhysicianHospitalWorkingTime.objects.all().filter(hide=False)
    if request.method == 'POST':
        work_time = get_object_or_none(physician_hospital_working_times, id=request.POST.get('id'))
        if work_time:
            work_time.hide = True
            work_time.save()

    context = {
        "physician_hospital_working_times": physician_hospital_working_times,
    }
    return render(request, 'cpanel/Hospital/Physician_Hospital_working_time_list.html', context)
