from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from cpanel.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def Insurance_Company_add(request):
    if request.is_ajax():
        if request.method == 'POST':
            if get_object_or_none(InsuranceCompanies, company_id=request.POST.get('company_id')):
                return HttpResponseNotFound("This Insurance Company data is already stored")

            hide = True if request.POST.get('hide') == 'on' else False

            user = User.objects.create_user(
                username=request.POST.get('company_id'),
                password=request.POST.get('password')
            )

            # Add user to the group
            group = Group.objects.get(name='Insurance Company')
            group.user_set.add(user)

            company = InsuranceCompanies.objects.create(
                company_id=request.POST.get('company_id'),
                email=request.POST.get('email'),
                fax=request.POST.get('fax'),
                company_name=request.POST.get('company_name'),
                company_type=request.POST.get('company_type'),
                hide=hide,
                user=user
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

    if request.is_ajax():
        if request.method == "POST":
            # data preprocessing
            hide = True if request.POST.get('hide') == 'on' else False

            # Handle insurance company
            insurance_company.company_id = request.POST.get('company_id')
            insurance_company.email = request.POST.get('email')
            insurance_company.fax = request.POST.get('fax')
            insurance_company.company_name = request.POST.get('company_name')
            insurance_company.company_type = request.POST.get('company_type')
            insurance_company.hide = hide

            insurance_company.save()

            # Handle password
            if request.POST.get('password'):
                user = get_object_or_none(User, username=insurance_company)
                if user.check_password(request.POST.getlist('password')[0]):
                    user.set_password(request.POST.getlist('password')[1])
                    user.save()

            # Handle phone
            old_numbers = [i.phone for i in insurance_company_numbers]
            for number in request.POST.getlist('phone'):
                if number in old_numbers:
                    old_numbers.remove(number)
                else:
                    InsuranceCompaniesPhone.objects.create(
                        company=insurance_company,
                        phone=number
                    )
            delete_phones = [i for i in insurance_company_numbers if i.phone in old_numbers]
            for instance in delete_phones:
                instance.delete()

            # Handle address
            old_address = [i.address for i in insurance_company_address]
            for address in request.POST.getlist('address'):
                if address in old_address:
                    old_address.remove(address)
                else:
                    InsuranceCompaniesAddress.objects.create(
                        company=insurance_company,
                        address=address
                    )
            delete_address = [i for i in insurance_company_address if i.address in old_address]
            for instance in delete_address:
                instance.delete()

    context = {
        'insurance_company': insurance_company,
        'main_phone': insurance_company_numbers[0].phone,
        'phones': insurance_company_numbers[1:],
        'main_address': insurance_company_address[0].address,
        'address': insurance_company_address[1:],

    }
    return render(request, 'cpanel/Insurance Company/Insurance_Company_edit.html', context)


def Insurance_Company_list(request):
    insurance_companies = InsuranceCompanies.objects.all().filter(hide=False)
    if request.method == 'POST':
        insurance_company = get_object_or_none(InsuranceCompanies, company_id=request.POST.get('id'))
        if insurance_company:
            insurance_company.hide = True
            insurance_company.save()

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
    if request.is_ajax():
        if request.method == "POST":
            hide = True if request.POST.get('hide') == 'on' else False
            insurance_type.type_name = request.POST.get('type_name')
            insurance_type.hide = hide

            insurance_type.save()

            return HttpResponse()

    context = {
        'insurance_type': insurance_type,
    }
    return render(request, 'cpanel/Insurance Company/Insurance_Type_edit.html', context)


def Insurance_Type_list(request):
    insurance_types = InsuranceTypes.objects.all().filter(hide=False)
    if request.method == 'POST':
        InsuranceType = get_object_or_none(InsuranceTypes, type_id=request.POST.get('id'))
        if InsuranceType:
            InsuranceType.hide = True
            InsuranceType.save()

    context = {
        "insurance_types": insurance_types,
    }
    return render(request, 'cpanel/Insurance Company/Insurance_Type_list.html', context)
