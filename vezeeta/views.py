from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.core import serializers
import operator
from .recommendation import *
import numpy as np
import math
from collections import OrderedDict
from .recommendation import *


def Doctor_Details(request, NN):
    # AI recommendation functions call
    Save_All_Doctors_In_Recommendation_Data_Base(NN)
    current_doctor_data = Return_Doctor_Details_For_Recommendation(NN)
    KNN_List = main(current_doctor_data)
    KNN_List_Cleared = []
    counter = 0
    addresses = []
    rates = []
    fees = []
    bookings = []
    titles = []
    images = []
    if KNN_List:
        for i in KNN_List:
            if KNN_List[counter] == None:
                counter += 1
            else:
                KNN_List_Cleared.append(KNN_List[counter])
                nn = KNN_List[counter].physician_nn
                instance = get_object_or_404(Physician, physician_nn=nn)
                if PhysicianClinicWorkingTime.objects.filter(physician_nn=instance):
                    obj = PhysicianClinicWorkingTime.objects.filter(physician_nn=instance)
                    clinic = obj[0].clinic.clinic.institution_id
                    instance_clinic = MedicalInstitutions.objects.filter(institution_id=clinic)
                    addresss = instance_clinic[0].get_address
                    addresses.append(addresss[0].address)
                    # addresses.append(instance_clinic)
                else:
                    addresses.append(None)
                obj = PhysicianRecommendation.objects.filter(physician_nn=instance)
                print(obj)
                rate = obj[0].rating
                fee = obj[0].fee
                fees.append(fee)
                booking = obj[0].booking_count
                bookings.append(booking)
                rates.append(rate)
                physician = Physician.objects.filter(physician_nn=instance)
                title = physician[0].title
                titles.append(title)
                stakeholder = Stakeholders.objects.filter(national_number=instance)
                image = stakeholder[0].image
                images.append(image)
                counter += 1
    # dictOf_KNN_Cleared = { i : KNN_List_Cleared[i] for i in range(0, len(KNN_List_Cleared) ) }
    full_list = zip(KNN_List_Cleared, addresses, rates, fees, bookings, titles, images)
    print(KNN_List_Cleared, addresses, rates, fees, bookings, titles, images)

    # ************************************************************ #
    if request.is_ajax() and request.method == 'GET':
       # handle visit location
        get_medical_institution_id = request.GET.get('code')
        medical_institution_address = MedicalInstitutionsAddress.objects.filter(institution=get_medical_institution_id)
        address = []
        for i in medical_institution_address:
            address.append(i.address)
        dictOfWords = {i: address[i] for i in range(0, len(address))}
        # handle location fee
        # clinic
        fee = []
        if PhysicianClinicWorkingTime.objects.filter(clinic=get_medical_institution_id):
            clinicFee = PhysicianClinicWorkingTime.objects.filter(clinic=get_medical_institution_id)
            for i in clinicFee:
                fee.append(i.fee)
            dictOfFee = {i: fee[i] for i in range(0, len(fee))}
            max_1 = max(dictOfFee.items(), key=operator.itemgetter(1))[0]
            fee = {'fees': dictOfFee[max_1]}
            dictOfWords.update(fee)

            # hospital
        if PhysicianHospitalWorkingTime.objects.filter(hospital=get_medical_institution_id):
            hospitalFee = PhysicianHospitalWorkingTime.objects.filter(hospital=get_medical_institution_id)
            for i in hospitalFee:
                fee.append(i.fee)
            dictOfFee = {i: fee[i] for i in range(0, len(fee))}
            max_1 = max(dictOfFee.items(), key=operator.itemgetter(1))[0]
            fee = {'fees': dictOfFee[max_1]}
            dictOfWords.update(fee)
        # handle phones of clinic and hospital
        phone = []
        if MedicalInstitutionsPhone.objects.filter(institution=get_medical_institution_id):
            medical_institution_phone = MedicalInstitutionsPhone.objects.filter(institution=get_medical_institution_id)
            for i in medical_institution_phone:
                phone.append(i.phone)
            dictOfPhones = {i: phone[i] for i in range(0, len(phone))}
            phone_final = {'phone': dictOfPhones[0]}
            dictOfWords.update(phone_final)
        # handle location mail
            # clinic
        mail = []
        if Clinic.objects.filter(clinic=get_medical_institution_id):
            clinicMail = Clinic.objects.filter(clinic=get_medical_institution_id)
            for i in clinicMail:
                mail.append(i.email)
            dictOfMail = {i: mail[i] for i in range(0, len(mail))}
            mail = {'mail': dictOfMail[0]}
            dictOfWords.update(mail)

            # hospital
        if Hospital.objects.filter(hospital=get_medical_institution_id):
            hospitalMail = Hospital.objects.filter(hospital=get_medical_institution_id)
            for i in hospitalMail:
                mail.append(i.email)
            dictOfMail = {i: mail[i] for i in range(0, len(mail))}
            mail = {'mail': dictOfMail[0]}
            dictOfWords.update(mail)

        # handle jason send whole data
        return JsonResponse(dictOfWords, safe=False)

    print(NN)
    doctor = get_object_or_404(Physician, physician_nn=NN)
    # handle clinicworkingtime
    physicianclinicworkingtime = PhysicianClinicWorkingTime.objects.filter(physician_nn=NN)
    clinic_id = None
    clinic = None
    if physicianclinicworkingtime[1:]:
        for clinic in physicianclinicworkingtime[1:]:
            first_clinic = clinic.clinic
            clinic_id = first_clinic.clinic
            clinic = get_object_or_404(Clinic, clinic=clinic_id)
    else:
        pass
    # handle hospitalworkingtime
    physicianhospitalworkingtime = PhysicianHospitalWorkingTime.objects.filter(physician_nn=NN)
    hospital_id = None
    hospital = None
    if physicianclinicworkingtime[1:]:
        for hospital in physicianhospitalworkingtime[1:]:
            first_hospital = hospital.hospital
            hospital_id = first_hospital.hospital
            hospital = get_object_or_404(Hospital, hospital=hospital_id)
    else:
        pass
    stakeholder = get_object_or_404(Stakeholders, national_number=NN)
    # handle rating
    physicianrating = None
    physicianratingcount = "no"
    if PhysicianRating.objects.filter(physician_nn=NN):
        physicianrating = PhysicianRating.objects.filter(physician_nn=NN)
        physicianratingcount = PhysicianRating.objects.filter(physician_nn=NN).count()
    # handle user as patient
    patient = request.user
    # stakeholder_user = get_object_or_404(Stakeholders, national_number=1)
    # patient_nn = get_object_or_404(Patient, patient_nn=stakeholder_user)
    context = {
        "doctor": doctor,
        'stakeholder': stakeholder,
        'physicianclinicworkingtime': physicianclinicworkingtime,
        'physicianhospitalworkingtime': physicianhospitalworkingtime,
        'clinic': clinic,
        'hospital': hospital,
        'physicianrating': physicianrating,
        'physicianratingcount': physicianratingcount,
        # 'stakeholder_user': stakeholder_user,
        # ********************** AI recommendation variables **********************
        'KNN_List': full_list,
        # 'addresses':addresses,
        # 'rates' :rates  ,
        # 'fees' : fees,
        # 'bookings': bookings ,
        # 'titles': titles,
        # 'images':images
    }

    if request.method == 'POST' and request.is_ajax():
        # handel if review ---------------------------------------
        if 'patient_comment_js' in request.POST:
            current_rate = request.POST['rate_js']
            comment = request.POST['patient_comment_js']
            patient_nn_js = request.POST['patient_nn_js']
            patient_nn_js = request.POST['physician_nn_js']
            if patient_nn_js:
                rate = PhysicianRating.objects.filter(patient_nn=patient_nn_js).update(rate=current_rate)
            if current_rate:
                user_rating = PhysicianRating.objects.create(
                    patient_nn=patient_nn,
                    physician_nn=doctor,
                    patient_comment=comment,
                    rate=current_rate,
                )
                return HttpResponse()
        # if booking ---------------------------------------
    if request.method == 'POST' and request.is_ajax():
        if 'message' in request.POST:
            message = request.POST.get('message'),
            if message:
                booking = PhysicianPatientBooking.objects.create(
                    patient_nn=patient_nn,
                    physician_nn=doctor,
                    booking_date_clinic="2020-02-25",
                    booking_date_hospital="2020-02-25",
                    clinic=clinic,
                    hospital=hospital,
                    phone=request.POST.get('phone'),
                    email=request.POST.get('email'),
                    message=message,
                )

                return HttpResponse()

    return render(request, 'vezeeta/doctor/Doctor_Details.html', context)


def Clinic_Details(request, id):

    if request.is_ajax() and request.method == 'GET':
        # handle clinic fee
        dictOfWords = {}
        get_physician_nn = request.GET.get('code')
        fee = []
        if PhysicianClinicWorkingTime.objects.filter(physician_nn=get_physician_nn):
            clinicFee = PhysicianClinicWorkingTime.objects.filter(physician_nn=get_physician_nn)
            for i in clinicFee:
                fee.append(i.fee)
            dictOfFee = {i: fee[i] for i in range(0, len(fee))}
            max_1 = max(dictOfFee.items(), key=operator.itemgetter(1))[0]
            fee = {'fees': dictOfFee[max_1]}
            dictOfWords.update(fee)

        return JsonResponse(dictOfWords, safe=False)

    clinic = get_object_or_404(Clinic, clinic=id)
    medicalinstitution = get_object_or_404(MedicalInstitutions, institution_id=id)
    # handle rating
    clinicrating = None
    clinicratingcount = "No"
    if ClinicRating.objects.filter(clinic=id):
        clinicrating = ClinicRating.objects.filter(clinic=id)
        clinicratingcount = ClinicRating.objects.filter(clinic=id).count()
    # handle user as patient
    patient = request.user
    stakeholder_user = get_object_or_404(Stakeholders, national_number=patient)
    patient_nn = get_object_or_404(Patient, patient_nn=stakeholder_user)
    # handle clinicworkingtime
    physicianclinicworkingtime = PhysicianClinicWorkingTime.objects.filter(clinic=id)
    specialization_list = []
    for doctor in physicianclinicworkingtime:
        stakeholder = get_object_or_404(Stakeholders, national_number=doctor)
        doctor = get_object_or_404(Physician, physician_nn=stakeholder)
        specialization_list.append(PhysicianSpecialization.objects.filter(physician_nn=doctor))

    context = {
        'clinic': clinic,
        'medicalinstitution': medicalinstitution,
        'clinicrating': clinicrating,
        'clinicratingcount': clinicratingcount,
        'stakeholder_user': stakeholder_user,
        'physicianclinicworkingtime': physicianclinicworkingtime,
        'specialization_list': specialization_list,

    }

    if request.method == 'POST' and request.is_ajax():
        # handel if review ---------------------------------------
        if 'patient_comment_js' in request.POST:
            current_rate = request.POST.get('rate_js')
            comment = request.POST.get('patient_comment_js')
            if patient_nn:
                rate = ClinicRating.objects.filter(patient_nn=patient_nn).update(rate=current_rate)
            if current_rate:
                user_rating = ClinicRating.objects.create(
                    patient_nn=patient_nn,
                    clinic=clinic,
                    patient_comment=comment,
                    rate=current_rate
                )
                return HttpResponse()

        # if booking ---------------------------------------
    if request.method == 'POST' and request.is_ajax():
        if 'message' in request.POST:
            selected_doctor = request.POST.get('physician_nn')
            selected_doctor_instance = get_object_or_404(Physician, physician_nn=selected_doctor)
            message = request.POST.get('message')
            if message:
                booking = ClinicPatientBooking.objects.create(
                    patient_nn=patient_nn,
                    physician_nn=selected_doctor_instance,
                    booking_date_clinic="2020-02-25",
                    clinic=clinic,
                    phone=request.POST.get('phone'),
                    email=request.POST.get('email'),
                    message=message,
                )
                return HttpResponse()

    return render(request, 'vezeeta/clinic/Clinic_Details.html', context)


def Hospital_Details(request, id):

    if request.is_ajax() and request.method == 'GET':
        # handle clinic fee
        dictOfWords = {}
        get_physician_nn = request.GET.get('code')
        fee = []
        if PhysicianHospitalWorkingTime.objects.filter(physician_nn=get_physician_nn):
            hospitalFee = PhysicianHospitalWorkingTime.objects.filter(physician_nn=get_physician_nn)
            for i in hospitalFee:
                fee.append(i.fee)
            dictOfFee = {i: fee[i] for i in range(0, len(fee))}
            max_1 = max(dictOfFee.items(), key=operator.itemgetter(1))[0]
            fee = {'fees': dictOfFee[max_1]}
            dictOfWords.update(fee)

        return JsonResponse(dictOfWords, safe=False)

    hospital = get_object_or_404(Hospital, hospital=id)
    medicalinstitution = get_object_or_404(MedicalInstitutions, institution_id=id)
    # handle rating
    hospitalrating = None
    hospitalratingcount = "No"
    if HospitalRating.objects.filter(hospital=id):
        hospitalrating = HospitalRating.objects.filter(hospital=id)
        hospitalratingcount = HospitalRating.objects.filter(hospital=id).count()
    # handle user as patient
    patient = request.user
    stakeholder_user = get_object_or_404(Stakeholders, national_number=patient)
    patient_nn = get_object_or_404(Patient, patient_nn=stakeholder_user)
    # handle clinicworkingtime
    physicianhospitalworkingtime = PhysicianHospitalWorkingTime.objects.filter(hospital=id)
    specialization_list = []
    for doctor in physicianhospitalworkingtime:
        stakeholder = get_object_or_404(Stakeholders, national_number=doctor)
        doctor = get_object_or_404(Physician, physician_nn=stakeholder)
        specialization_list.append(PhysicianSpecialization.objects.filter(physician_nn=doctor))

    context = {
        'hospital': hospital,
        'medicalinstitution': medicalinstitution,
        'hospitalrating': hospitalrating,
        'hospitalratingcount': hospitalratingcount,
        'stakeholder_user': stakeholder_user,
        'physicianhospitalworkingtime': physicianhospitalworkingtime,
        'specialization_list': specialization_list,

    }

    if request.method == 'POST' and request.is_ajax():
        # handel if review ---------------------------------------
        if 'patient_comment_js' in request.POST:
            current_rate = request.POST.get('rate_js')
            comment = request.POST.get('patient_comment_js')
            if patient_nn:
                rate = HospitalRating.objects.filter(patient_nn=patient_nn).update(rate=current_rate)
            if current_rate:
                user_rating = HospitalRating.objects.create(
                    patient_nn=patient_nn,
                    hospital=hospital,
                    patient_comment=comment,
                    rate=current_rate
                )
                return HttpResponse()

        # if booking ---------------------------------------
    if request.method == 'POST' and request.is_ajax():
        if 'message' in request.POST:
            selected_doctor = request.POST.get('physician_nn')
            selected_doctor_instance = get_object_or_404(Physician, physician_nn=selected_doctor)
            message = request.POST.get('message')
            if message:
                booking = HospitalPatientBooking.objects.create(
                    patient_nn=patient_nn,
                    physician_nn=selected_doctor_instance,
                    booking_date_hospital="2020-02-25",
                    hospital=hospital,
                    phone=request.POST.get('phone'),
                    email=request.POST.get('email'),
                    message=message,
                )
                return HttpResponse()

    return render(request, 'vezeeta/hospital/Hospital_Details.html', context)
