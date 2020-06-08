from django import template
from django.contrib.auth.models import User
from main.utils import get_object_or_none
from cpanel.models import *

register = template.Library()


@register.filter
def my_range(value):
    return [0] * value


@register.filter
def my_pages(value, total):
    value = int(value)
    total = int(total)
    if value == 1:
        end = (value + 4) if total > (value + 4) else total + 1
        return [i for i in range(value, end)]
    elif value == 2:
        end = (value + 3) if total > (value + 3) else total + 1
        return [i for i in range(1, end)]
    else:
        end = (value + 3) if total > (value + 3) else total + 1
        return [i for i in range(value - 2, end)]


@register.filter
def into_str(value):
    return str(value)


@register.filter
def into_int(value):
    return int(value)


@register.filter
def into_list(value):
    try:
        value = value.split(',')
        return value
    except Exception:
        return value


@register.filter
def add(value, add):
    return int(value) + int(add)


@register.filter
def sub(value, add):
    return int(value) - int(add)


@register.filter
def label(value):
    value = value.capitalize().split('_')
    value = ' '.join(value)
    return value


@register.filter
def get_name(value):
    user = get_object_or_none(User, username=value)
    stakeholder = get_object_or_none(Stakeholders, user=user)
    name = None
    if stakeholder:
        name = stakeholder.stakeholder_name
    else:
        medical_institution = get_object_or_none(MedicalInstitutions, user=user)
        if medical_institution:
            name = medical_institution.institution_name
        else:
            insurance_company = get_object_or_none(InsuranceCompanies, user=user)
            if insurance_company:
                name = insurance_company.company_name

    return name


@register.filter
def get_image_url(value):
    user = get_object_or_none(User, username=value)
    stakeholder = get_object_or_none(Stakeholders, user=user)
    name = None
    if stakeholder:
        image = stakeholder.image.url
    else:
        medical_institution = get_object_or_none(MedicalInstitutions, user=user)
        if medical_institution:
            image = medical_institution.image.url
        else:
            insurance_company = get_object_or_none(InsuranceCompanies, user=user)
            if insurance_company:
                image = insurance_company.image.url
    return image


@register.filter
def allowed_users(user, allowed_groups):
    user = get_object_or_none(User, username=user)
    allowed_roles = allowed_groups.split(',')

    if user:
        group = user.groups.filter(name__in=allowed_roles).exists()
        return group
    return None
