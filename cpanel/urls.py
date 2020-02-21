from django.urls import path
from . import views
from . import autodb


app_name = 'cpanel'
urlpatterns = [
    # Doctors URLs
    path('doctor_add/', views.Doctor_add, name='doctor_add'),
    path('doctor_edit/<NN>/', views.Doctor_edit, name='doctor_edit'),
    path('doctor_list/', views.Doctor_list, name='doctor_list'),
    # Patients URLs
    path('patient_add/', views.Patient_add, name='patient_add'),
    path('patient_edit/<NN>/', views.Patient_edit, name='patient_edit'),
    path('patient_list/', views.Patient_list, name='patient_list'),
    # Patients History URLs
    path('patient_history_add/', views.Patient_history_add, name='patient_history_add'),
    path('patient_history_edit/<id>/', views.Patient_history_edit, name='patient_history_edit'),
    path('patient_history_list/', views.Patient_history_list, name='patient_history_list'),
    # Nurse URLs
    path('nurse_add/', views.Nurse_add, name='nurse_add'),
    path('nurse_edit/<NN>/', views.Nurse_edit, name='nurse_edit'),
    path('nurse_list/', views.Nurse_list, name='nurse_list'),
    # Paramedic URLs
    path('paramedic_add/', views.Paramedic_add, name='paramedic_add'),
    path('paramedic_edit/<NN>/', views.Paramedic_edit, name='paramedic_edit'),
    path('paramedic_list/', views.Paramedic_list, name='paramedic_list'),
    # Parmacist URLs
    path('pharmacist_add/', views.Pharmacist_add, name='pharmacist_add'),
    path('pharmacist_edit/<NN>/', views.Pharmacist_edit, name='pharmacist_edit'),
    path('pharmacist_list/', views.Pharmacist_list, name='phaarmacist_list'),
    # Specialist URLs
    path('specialist_add/', views.Specialist_add, name='specialist_add'),
    path('specialist_edit/<NN>/', views.Specialist_edit, name='specialist_edit'),
    path('specialist_list/', views.Specialist_list, name='specialist_list'),
    # Specialization URLs
    path('specialization_add/', views.Specialization_add, name='specialization_add'),
    path('specialization_edit/<id>/', views.Specialization_edit, name='specialization_edit'),
    path('specialization_list/', views.Specialization_list, name='specialization_list'),
    # Stakeholder URLs
    path('stakeholder_add/', views.Stakeholder_add, name='stakeholder_add'),
    path('stakeholder_edit/<NN>/', views.Stakeholder_edit, name='stakeholder_edit'),
    path('stakeholder_list/', views.Stakeholder_list, name='stakeholder_list'),
    # Clinic URLs
    path('clinic_add/', views.Clinic_add, name='clinic_add'),
    path('clinic_edit/<id>/', views.Clinic_edit, name='clinic_edit'),
    path('clinic_list/', views.Clinic_list, name='clinic_list'),
    # Pharmacy URLs
    path('pharmacy_add/', views.Pharmacy_add, name='pharmacy_add'),
    path('pharmacy_edit/<id>/', views.Pharmacy_edit, name='pharmacy_edit'),
    path('pharmacy_list/', views.Pharmacy_list, name='pharmacy_list'),
    # Physician Clinic Working Time URLs
    path('physician_clinic_working_time_add/', views.Physician_Clinic_Working_Time_add, name='physician_clinic_working_time_add'),
    path('physician_clinic_working_time_edit/', views.Physician_Clinic_Working_Time_edit, name='physician_clinic_working_time_edit'),
    path('physician_clinic_working_time_list/', views.Physician_Clinic_Working_Time_list, name='physician_clinic_working_time_list'),
    # Hospital URLs
    path('hospital_add/', views.Hospital_add, name='hospital_add'),
    path('hospital_edit/<id>/', views.Hospital_edit, name='hospital_edit'),
    path('hospital_list/', views.Hospital_list, name='hospital_list'),
    # Physician Hospital Working Time URLs
    path('physician_hospital_working_time_add/', views.Physician_Hospital_Working_Time_add, name='physician_hospital_working_time_add'),
    path('physician_hospital_working_time_edit/', views.Physician_Hospital_Working_Time_edit, name='physician_hospital_working_time_edit'),
    path('physician_hospital_working_time_list/', views.Physician_Hospital_Working_Time_list, name='physician_hospital_working_time_list'),

    # Insurance Company URLS
    path('insurance_company_add/', views.Insurance_Company_add, name='insurance_company_add'),
    path('insurance_company_edit/<id>/', views.Insurance_Company_edit, name='insurance_company_edit'),
    path('insurance_company_list/', views.Insurance_Company_list, name='insurance_company_list'),
    # Insurance Type URLS
    path('insurance_type_add/', views.Insurance_Type_add, name='insurance_type_add'),
    path('insurance_type_edit/<id>/', views.Insurance_Type_edit, name='insurance_type_edit'),
    path('insurance_type_list/', views.Insurance_Type_list, name='insurance_type_list'),
    # Lab URLs
    path('lab_add/', views.Lab_add, name='lab_add'),
    path('lab_edit/<id>/', views.Lab_edit, name='lab_edit'),
    path('lab_list/', views.Lab_list, name='lab_list'),
    # Medical Institution URLs
    path('medical_institution_add/', views.Medical_Institution_add, name='medical_institution_add'),
    path('medical_institution_edit/<id>/', views.Medical_Institution_edit, name='medical_institution_edit'),
    path('medical_institution_list/', views.Medical_Institution_list, name='medical_institution_list'),
    # Data Entery Automation
    path('add_groups/', autodb.group_add),
    path('add_specialization/', autodb.specialization_add)
]
