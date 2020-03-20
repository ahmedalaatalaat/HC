from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from .models import *


# Doctor Views
def Doctor_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST)
            if get_object_or_none(Physician, physician_nn=request.POST.get('national_number')):
                return HttpResponseNotFound("This doctor data is already stored")

            # data preprocessing
            hide = True if request.POST.get('hide') == 'on' else False
            date = request.POST.get('birthday').split('-')
            date = f'{date[2]}-{date[0]}-{date[1]}'

            stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('national_number'))
            if not stakeholder:
                stakeholder = Stakeholders.objects.create(
                    stakeholder_name=request.POST.get('stakeholder_name'),
                    national_number=request.POST.get('national_number'),
                    stakeholder_last_name=request.POST.get('stakeholder_last_name'),
                    password=request.POST.get('password'),
                    birthday=date,
                    gender=request.POST.get('gender'),
                    email=request.POST.get('email'),
                    marital_status=request.POST.get('marital_status'),
                    nationality=request.POST.get('nationality'),
                    cv=request.POST.get('cv'),
                    image=request.FILES.get('image')
                )

            physician = Physician.objects.create(
                physician_nn=stakeholder,
                title=request.POST.get('title'),
                hide=hide
            )

            for specialization in request.POST.getlist('specialization'):
                PhysicianSpecialization.objects.create(
                    physician_nn=physician,
                    specialization=specialization
                )

            for phone in request.POST.getlist('Phone'):
                StakeholdersPhones.objects.create(
                    national_number=stakeholder,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                StakeholdersAddress.objects.create(
                    national_number=stakeholder,
                    address=address
                )

            return HttpResponse()
    return render(request, 'cpanel/Doctor/Doctor_add.html')


def Doctor_edit(request, NN):
    stakeholder = get_object_or_404(Stakeholders, national_number=NN)
    stakeholder_numbers = stakeholder.get_phone
    stakeholder_address = stakeholder.get_address
    doctor = get_object_or_404(Physician, physician_nn=NN)
    context = {
        'stakeholder': stakeholder,
        'main_phone': stakeholder_numbers[0],
        'phones': stakeholder_numbers[1:],
        'main_address': stakeholder_address[0],
        'address': stakeholder_address[1:],
        'doctor': doctor,
    }
    return render(request, 'cpanel/Doctor/Doctor_edit.html', context)


def Doctor_list(request):
    doctors = Physician.objects.all()
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
                date = request.POST.get('birthday').split('-')
                date = f'{date[2]}-{date[0]}-{date[1]}'
                stakeholder = Stakeholders.objects.create(
                    stakeholder_name=request.POST.get('stakeholder_name'),
                    national_number=request.POST.get('national_number'),
                    stakeholder_last_name=request.POST.get('stakeholder_last_name'),
                    password=request.POST.get('password'),
                    birthday=date,
                    gender=request.POST.get('gender'),
                    email=request.POST.get('email'),
                    marital_status=request.POST.get('marital_status'),
                    nationality=request.POST.get('nationality'),
                    cv=request.POST.get('cv'),
                    image=request.FILES.get('image')
                )

            print(hide)
            patient = Patient.objects.create(
                patient_nn=stakeholder,
                blood_type=request.POST.get('blood_type'),
                chronic_diseases_name=request.POST.get('chronic_diseases_name'),
                chronic_diseases_type=request.POST.get('chronic_diseases_type'),
                hide=hide
            )

            for phone in request.POST.getlist('Phone'):
                StakeholdersPhones.objects.create(
                    national_number=stakeholder,
                    phone=phone
                )
            for phone in request.POST.getlist('relatives_phones'):
                PatientRelativesPhones.objects.create(
                    patient_nn=patient,
                    phone=phone
                )
            for address in request.POST.getlist('address'):
                StakeholdersAddress.objects.create(
                    national_number=stakeholder,
                    address=address
                )

            return HttpResponse()
    return render(request, 'cpanel/Patient/Patient_add.html')


def Patient_edit(request, NN):
    pass


def Patient_list(request):
    patients = Patient.objects.all()
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
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Nurse, nurse_nn=request.POST.get('national_number')):
                return HttpResponseNotFound("This Nurse data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            stakeholder = get_object_or_none(Stakeholders, national_number=request.POST.get('national_number'))
            if not stakeholder:
                date = request.POST.get('birthday').split('-')
                date = f'{date[2]}-{date[0]}-{date[1]}'
                stakeholder = Stakeholders.objects.create(
                    stakeholder_name=request.POST.get('stakeholder_name'),
                    national_number=request.POST.get('national_number'),
                    stakeholder_last_name=request.POST.get('stakeholder_last_name'),
                    password=request.POST.get('password'),
                    birthday=date,
                    gender=request.POST.get('gender'),
                    email=request.POST.get('email'),
                    marital_status=request.POST.get('marital_status'),
                    nationality=request.POST.get('nationality'),
                    cv=request.POST.get('cv'),
                    image=request.FILES.get('image')
                )

            nurse = Nurse.objects.create(
                nurse_nn=stakeholder,
                hide=hide
            )

            for phone in request.POST.getlist('Phone'):
                StakeholdersPhones.objects.create(
                    national_number=stakeholder,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                StakeholdersAddress.objects.create(
                    national_number=stakeholder,
                    address=address
                )
            for specialization in request.POST.getlist('specialization'):
                NurseSpecialization.objects.create(
                    nurse_nn=nurse,
                    specialization=specialization
                )

            return HttpResponse()
    return render(request, 'cpanel/Nurse/Nurse_add.html')


def Nurse_edit(request, NN):
    pass


def Nurse_list(request):
    nurses = Nurse.objects.all()
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
                date = request.POST.get('birthday').split('-')
                date = f'{date[2]}-{date[0]}-{date[1]}'
                stakeholder = Stakeholders.objects.create(
                    stakeholder_name=request.POST.get('stakeholder_name'),
                    national_number=request.POST.get('national_number'),
                    stakeholder_last_name=request.POST.get('stakeholder_last_name'),
                    password=request.POST.get('password'),
                    birthday=date,
                    gender=request.POST.get('gender'),
                    email=request.POST.get('email'),
                    marital_status=request.POST.get('marital_status'),
                    nationality=request.POST.get('Nationality'),
                    cv=request.POST.get('cv'),
                    image=request.FILES.get('image')
                )

            paramedic = Paramedic.objects.create(
                paramedic_nn=stakeholder,
                ambulance_palte_number=request.POST.get('ambulance_palte_number'),
                hide=hide
            )

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

            return HttpResponse()

    return render(request, 'cpanel/Paramedic/Paramedic_add.html')


def Paramedic_edit(request, NN):
    pass


def Paramedic_list(request):
    paramedics = Paramedic.objects.all()
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
                date = request.POST.get('birthday').split('-')
                date = f'{date[2]}-{date[0]}-{date[1]}'
                stakeholder = Stakeholders.objects.create(
                    stakeholder_name=request.POST.get('stakeholder_name'),
                    national_number=request.POST.get('national_number'),
                    stakeholder_last_name=request.POST.get('stakeholder_last_name'),
                    password=request.POST.get('password'),
                    birthday=date,
                    gender=request.POST.get('gender'),
                    email=request.POST.get('email'),
                    marital_status=request.POST.get('marital_status'),
                    nationality=request.POST.get('nationality'),
                    cv=request.POST.get('cv'),
                    image=request.FILES.get('image')
                )

            pharmacist = Pharmacist.objects.create(
                pharmacist_nn=stakeholder,
                hide=hide
            )

            for phone in request.POST.getlist('Phone'):
                StakeholdersPhones.objects.create(
                    national_number=stakeholder,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                StakeholdersAddress.objects.create(
                    national_number=stakeholder,
                    address=address
                )
            for specialization in request.POST.getlist('pharmacist_specialization'):
                PharmacistSpecialization.objects.create(
                    pharmacist_nn=pharmacist,
                    specialization=specialization
                )

            return HttpResponse()
    return render(request, 'cpanel/Pharmacist/Pharmacist_add.html')


def Pharmacist_edit(request, NN):
    pass


def Pharmacist_list(request):
    pharmacists = Pharmacist.objects.all()
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
                date = request.POST.get('birthday').split('-')
                date = f'{date[2]}-{date[0]}-{date[1]}'
                stakeholder = Stakeholders.objects.create(
                    stakeholder_name=request.POST.get('stakeholder_name'),
                    national_number=request.POST.get('national_number'),
                    stakeholder_last_name=request.POST.get('stakeholder_last_name'),
                    password=request.POST.get('password'),
                    birthday=date,
                    gender=request.POST.get('gender'),
                    email=request.POST.get('email'),
                    marital_status=request.POST.get('marital_status'),
                    nationality=request.POST.get('nationality'),
                    cv=request.POST.get('cv'),
                    image=request.FILES.get('image')
                )

            specialist = Specialist.objects.create(
                specialist_nn=stakeholder,
                hide=hide
            )

            for phone in request.POST.getlist('Phone'):
                StakeholdersPhones.objects.create(
                    national_number=stakeholder,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                StakeholdersAddress.objects.create(
                    national_number=stakeholder,
                    address=address
                )
            for specialization in request.POST.getlist('specialization'):
                SpecialistSpecialization.objects.create(
                    specialist_nn=specialist,
                    specialization=specialization
                )

            return HttpResponse()
    return render(request, 'cpanel/Specialist/Specialist_add.html')


def Specialist_edit(request, NN):
    pass


def Specialist_list(request):
    specialists = Specialist.objects.all()
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
                stakeholder = Stakeholders.objects.create(
                    stakeholder_name=request.POST.get('stakeholder_name'),
                    national_number=request.POST.get('national_number'),
                    stakeholder_last_name=request.POST.get('stakeholder_last_name'),
                    password=request.POST.get('password'),
                    birthday=request.POST.get('birthday'),
                    gender=request.POST.get('gender'),
                    email=request.POST.get('email'),
                    marital_status=request.POST.get('marital_status'),
                    nationality=request.POST.get('nationality'),
                    cv=request.POST.get('cv'),
                    image=request.FILES.get('image'),
                    stakeholder_type=request.POST.get('stakeholder_type'),
                )

            for phone in request.POST.getlist('Phone'):
                StakeholdersPhones.objects.create(
                    national_number=stakeholder,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                StakeholdersAddress.objects.create(
                    national_number=stakeholder,
                    address=address
                )

            return HttpResponse()
    return render(request, 'cpanel/Stakeholders/Stakeholders_add.html')


def Stakeholder_edit(request, NN):
    pass


def Stakeholder_list(request):
    stakeholders = Stakeholders.objects.all()
    context = {
        "stakeholders": stakeholders,
    }
    return render(request, 'cpanel/Stakeholders/Stakeholders_list.html', context)


# Clinic Views
def Clinic_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(Clinic, clinic=request.POST.get('clinic')):
                return HttpResponseNotFound("This Clinic data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False
            ER = True if request.POST.get('er_availability') == 'on' else False

            Medical_Institutions = MedicalInstitutions.objects.create(
                institution_id=request.POST.get('institution_id'),
                image=request.FILES.get('image'),
                institution_name=request.POST.get('institution_name'),
                hide=hide,
            )

            for phone in request.POST.getlist('phone'):
                MedicalInstitutionsPhone.objects.create(
                    institution=Medical_Institutions,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                MedicalInstitutionsAddress.objects.create(
                    institution=Medical_Institutions,
                    address=address
                )
            print(request.POST.get('er_availability'))
            Clinic.objects.create(
                clinic=Medical_Institutions,
                email=request.POST.get('email'),
                fax=request.POST.get('fax'),
                er_availability=ER,
                hide=hide,
            )

            return HttpResponse()

    return render(request, 'cpanel/Clinic/Clinic_add.html')


def Clinic_edit(request, id):
    institution = get_object_or_404(MedicalInstitutions, institution_id=id)
    institution_numbers = institution.get_phone
    institution_address = institution.get_address



    clinic =  get_object_or_404(Clinic, clinic=id)

    context = {
        'institution': institution,
        'main_phone': institution_numbers[0],
        'phones': institution_numbers[1:],
        'main_address': institution_address[0],
        'address': institution_address[1:],
        'clinic': clinic,
        
    }

    return render(request, 'cpanel/Clinic/Clinic_edit.html', context)


def Clinic_list(request):
    clinics = Clinic.objects.all()
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
                MedicalInstitutionsPhone.objects.create(
                    institution=Medical_Institutions,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                MedicalInstitutionsAddress.objects.create(
                    institution=Medical_Institutions,
                    address=address
                )

            owner = get_object_or_none(Pharmacist, pharmacist_nn=request.POST.get('owner'))
            print(request.POST.get('owner'))
            if not owner:
                return HttpResponseNotFound("This Pharmacist data is not stored")

            Pharmacy.objects.create(
                pharmacy=Medical_Institutions,
                pharmacy_type=request.POST.get('pharmacy_type'),
                owner=owner,
                hide=hide,
            )

            return HttpResponse()

    return render(request, 'cpanel/Pharmacy/Pharmacy_add.html')


def Pharmacy_edit(request, id):
    institution = get_object_or_404(MedicalInstitutions, institution_id=id)
    institution_numbers = institution.get_phone
    institution_address = institution.get_address



    pharmacy =  get_object_or_404(Pharmacy, pharmacy=id)

    context = {
        'institution': institution,
        'main_phone': institution_numbers[0],
        'phones': institution_numbers[1:],
        'main_address': institution_address[0],
        'address': institution_address[1:],
        'pharmacy': pharmacy,
        
    }

    return render(request, 'cpanel/Pharmacy/Pharmacy_edit.html', context)



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

            Medical_Institutions = MedicalInstitutions.objects.create(
                institution_id=request.POST.get('institution_id'),
                image=request.FILES.get('image'),
                institution_name=request.POST.get('institution_name'),
                hide=hide,
            )

            for phone in request.POST.getlist('phone'):
                MedicalInstitutionsPhone.objects.create(
                    institution=Medical_Institutions,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                MedicalInstitutionsAddress.objects.create(
                    institution=Medical_Institutions,
                    address=address
                )
            
            lab = Labs.objects.create(
                lab=Medical_Institutions,
                email=request.POST.get('email'),
                fax=request.POST.get('fax'),
                hide=hide,
            )
            
            for radiologyandanalysis in request.POST.getlist('radiologyandanalysis'):
                LabsAnalysisAndRadiology.objects.create(
                    lab=lab,
                    analysis_and_radiology=radiologyandanalysis
                )
            

            return HttpResponse()

    return render(request, 'cpanel/Lab/Labs_add.html')


def Lab_edit(request, id):
    institution = get_object_or_404(MedicalInstitutions, institution_id=id)
    institution_numbers = institution.get_phone
    institution_address = institution.get_address



    lab =  get_object_or_404(Labs, lab=id)
    labsanalysisandradiology = lab.get_A_R

    context = {
        'institution': institution,
        'main_phone': institution_numbers[0],
        'phones': institution_numbers[1:],
        'main_address': institution_address[0],
        'address': institution_address[1:],
        'Lab': lab,
        'labsanalysisandradiology' : labsanalysisandradiology[0]
    }

    return render(request, 'cpanel/Lab/Labs_edit.html', context)

def Lab_list(request):
    labs = Labs.objects.all()
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

            Medical_Institutions = MedicalInstitutions.objects.create(
                institution_id=request.POST.get('institution_id'),
                image=request.FILES.get('image'),
                institution_name=request.POST.get('institution_name'),
                hide=hide,
            )

            for phone in request.POST.getlist('Phone'):
                MedicalInstitutionsPhone.objects.create(
                    institution=Medical_Institutions,
                    phone=phone
                )

            for address in request.POST.getlist('address'):
                MedicalInstitutionsAddress.objects.create(
                    institution=Medical_Institutions,
                    address=address
                )

            return HttpResponse()

    return render(request, 'cpanel/Medical Institutions/Medical_institution_add.html')


def Medical_Institution_edit(request, id):

    institution = get_object_or_404(MedicalInstitutions, institution_id=id)
    institution_numbers = institution.get_phone
    institution_address = institution.get_address


    

    context = {
        'institution': institution,
        'main_phone': institution_numbers[0],
        'phones': institution_numbers[1:],
        'main_address': institution_address[0],
        'address': institution_address[1:],
    }

    return render(request, 'cpanel/Medical Institutions/Medical_institution_edit.html', context)



def Medical_Institution_list(request):
    medical_institutions = MedicalInstitutions.objects.all()
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


def Physician_Clinic_Working_Time_edit(request,id):
    physicianclinicworkingtime = get_object_or_404(PhysicianClinicWorkingTime, pk=id)



    context = {
        'physicianclinicworkingtime': physicianclinicworkingtime,

    }




    return render(request, 'cpanel/Clinic/Physician_Clinic_working_time_edit.html', context)


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

            for phone in request.POST.getlist('Phone'):
                MedicalInstitutionsPhone.objects.create(
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

    institution = get_object_or_404(MedicalInstitutions, institution_id=id)
    institution_numbers = institution.get_phone
    institution_address = institution.get_address

    hospital = get_object_or_404(Hospital, hospital=id)

    
    context = {
        'institution': institution,
        'main_phone': institution_numbers[0],
        'phones': institution_numbers[1:],
        'main_address': institution_address[0],
        'address': institution_address[1:],
        'hospital': hospital,
    }

    # Part 4
    return render(request, 'cpanel/Hospital/Hospital_edit.html', context)


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


def Physician_Hospital_Working_Time_edit(request,id):
    physicianhospitalworkingtime = get_object_or_404(PhysicianHospitalWorkingTime, pk=id)



    context = {
        'physicianhospitalworkingtime': physicianhospitalworkingtime,

    }




    return render(request, 'cpanel/Hospital/Physician_Hospital_working_time_edit.html', context)

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
                InsuranceCompaniesPhone.objects.create(
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

    insurance_company = get_object_or_404(InsuranceCompanies, company_id=id)
    insurance_company_numbers = insurance_company.get_phone
    insurance_company_address = insurance_company.get_address

   
   

    context = {
        'insurance_company': insurance_company,
        'main_phone': insurance_company_numbers[0],
        'phones': insurance_company_numbers[1:],
        'main_address': insurance_company_address[0],
        'address': insurance_company_address[1:],
        
    }

    return render(request, 'cpanel/Insurance Company/Insurance_Company_edit.html', context)

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
    insurance_type = get_object_or_404(InsuranceTypes, type_id=id)


   
   

    context = {
        'insurance_type': insurance_type,
       
        
    }

    return render(request, 'cpanel/Insurance Company/Insurance_Type_edit.html', context)

def Insurance_Type_list(request):
    insurance_types = InsuranceTypes.objects.all()
    context = {
        "insurance_types": insurance_types,
    }
    return render(request, 'cpanel/Insurance Company/Insurance_Type_list.html', context)
