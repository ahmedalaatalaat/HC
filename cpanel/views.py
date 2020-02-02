from django.shortcuts import render
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


def Doctor_edit(request):
    pass


def Doctor_list(request):
    doctors = Physician.objects.all()
    context = {
        "doctors": doctors,
    }
    return render(request, 'cpanel/Doctor/Doctor_list.html', context)


# Patient Views
def Patient_add(request):
    return render(request, 'cpanel/Patient/Patient_add.html')


def Patient_edit(request):
    pass


def Patient_list(request):
    patients = Patient.objects.all()
    context = {
        "patients": patients,
    }
    return render(request, 'cpanel/Patient/Patient_list.html', context)


# Patient History Views
def Patient_history_add(request):
    return render(request, 'cpanel/Patient/Patient_History_add.html')


def Patient_history_edit(request):
    pass


def Patient_history_list(request):
    patients_history = PatientHistory.objects.all()
    context = {
        "patients_history": patients_history,
    }
    return render(request, 'cpanel/Patient/Patient_History_list.html', context)


# Nurse Views
def Nurse_add(request):
    return render(request, 'cpanel/Nurse/Nurse_add.html')


def Nurse_edit(request):
    pass


def Nurse_list(request):
    nurses = Nurse.objects.all()
    context = {
        "nurses": nurses,
    }
    return render(request, 'cpanel/Nurse/Nurse_list.html', context)


# Paramedic Views
def Paramedic_add(request):
    return render(request, 'cpanel/Paramedic/Paramedic_add.html')


def Paramedic_edit(request):
    pass


def Paramedic_list(request):
    paramedics = Paramedic.objects.all()
    context = {
        "paramedics": paramedics,
    }
    return render(request, 'cpanel/Paramedic/Paramedic_list.html', context)


# Paramedic Views
def Pharmacist_add(request):
    return render(request, 'cpanel/Pharmacist/Pharmacist_add.html')


def Pharmacist_edit(request):
    pass


def Pharmacist_list(request):
    pharmacists = Pharmacist.objects.all()
    context = {
        "pharmacists": pharmacists,
    }
    return render(request, 'cpanel/Pharmacist/Pharmacist_list.html', context)


# Specialist Views
def Specialist_add(request):
    return render(request, 'cpanel/Specialist/Specialist_add.html')


def Specialist_edit(request):
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


def Specialization_edit(request):
    pass


def Specialization_list(request):
    specializations = Specialization.objects.all()
    context = {
        "specializations": specializations,
    }
    return render(request, 'cpanel/Specializations/Specialization_list.html', context)


# Stakeholder Views
def Stakeholder_add(request):
    return render(request, 'cpanel/Stakeholders/Stakeholders_add.html')


def Stakeholder_edit(request):
    pass


def Stakeholder_list(request):
    stakeholders = Stakeholders.objects.all()
    context = {
        "stakeholders": stakeholders,
    }
    return render(request, 'cpanel/Stakeholders/Stakeholders_list.html', context)


# Clinic Views
def Clinic_add(request):
    return render(request, 'cpanel/Clinic/Clinic_add.html')


def Clinic_edit(request):
    pass


def Clinic_list(request):
    clinics = Clinic.objects.all()
    context = {
        "clinics": clinics,
    }
    return render(request, 'cpanel/Clinic/Clinic_list.html', context)


# Pharmacy Views
def Pharmacy_add(request):
    return render(request, 'cpanel/Pharmacy/Pharmacy_add.html')


def Pharmacy_edit(request):
    pass


def Pharmacy_list(request):
    pharmacies = Pharmacy.objects.all()
    context = {
        "pharmacies": pharmacies,
    }
    return render(request, 'cpanel/Pharmacy/Pharmacy_list.html', context)


# Lab Views
def Lab_add(request):
    return render(request, 'cpanel/Lab/Lab_list.html')


def Lab_edit(request):
    pass


def Lab_list(request):
    labs = Labs.objects.all()
    context = {
        "labs": labs,
    }
    return render(request, 'cpanel/Lab/Lab_list.html', context)


# Medical Institution Views
def Medical_Institution_add(request):
    return render(request, 'cpanel/Medical Institutions/Medical_institution_add.html')


def Medical_Institution_edit(request):
    pass


def Medical_Institution_list(request):
    medical_institutions = MedicalInstitutions.objects.all()
    context = {
        "medical_institutions": medical_institutions,
    }
    return render(request, 'cpanel/Medical Institutions/Medical_institution_list.html', context)


# Physician Clinic Working Time Views
def Physician_Clinic_Working_Time_add(request):
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
    return render(request, 'cpanel/Hospital/Hospital_add.html')


def Hospital_edit(request):
    pass


def Hospital_list(request):
    hospitals = Hospital.objects.all()
    context = {
        "hospitals": hospitals,
    }
    return render(request, 'cpanel/Hospital/Hospital_list.html', context)


# Physician Hospital Working Time Views
def Physician_Hospital_Working_Time_add(request):
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
    return render(request, 'cpanel/Insurance Company/Insurance_Company_add.html')


def Insurance_Company_edit(request):
    pass


def Insurance_Company_list(request):
    insurance_companies = InsuranceCompanies.objects.all()
    context = {
        "insurance_companies": insurance_companies,
    }
    return render(request, 'cpanel/Insurance Company/Insurance_Company_list.html', context)


# Insurance Type Views
def Insurance_Type_add(request):
    return render(request, 'cpanel/Insurance Company/Insurance_Type_add.html')


def Insurance_Type_edit(request):
    pass


def Insurance_Type_list(request):
    insurance_types = InsuranceTypes.objects.all()
    context = {
        "insurance_types": insurance_types,
    }
    return render(request, 'cpanel/Insurance Company/Insurance_Type_list.html', context)
