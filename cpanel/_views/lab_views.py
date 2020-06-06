from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from cpanel.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Q
from cpanel.decorators import *

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

@allowed_users(['Admin', 'Physician' , 'Nurse' , 'Specialist','Labs'])
def Lab_list(request):
    if str(request.user.groups.all().first()) == 'Nurse':
        labs = set()
        user = request.user
        labNurses =LabNurses.objects.all().filter(
            Q(nurse_nn__nurse_nn__user=user)).distinct()
        for nurses in labNurses:
            labs.add(nurses.lab)

    elif str(request.user.groups.all().first()) ==  'Specialist':
        labs = set()
        user = request.user
        labSpecialists =LabSpecialists.objects.all().filter(
            Q(specialist_nn__specialist_nn__user=user)).distinct()
        for specialists in labSpecialists:
            labs.add(specialists.lab)
    else :    
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
