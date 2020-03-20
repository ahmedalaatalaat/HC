# ------------------ if stakeholder: ---------------------------

# part 1
if request.is_ajax():
    if request.method == 'POST':
        if get_object_or_none(StakeholderType, StakeholderTypeID=request.POST.get('StakeholderTypeID')):
            return HttpResponseNotFound("This StakeholderType data is already stored")

        hide = True if request.POST.get('hide') == 'on' else False

# part 2 # Put it as it's
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
        image=request.FILES.get('image')
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

# part 3
StakeholderType.objects.create(
    # StakeholderType data
)

# Part 4
return HttpResponse()


# ------------------ if Medical Institutions --------------

# Part 1
if request.is_ajax():
    if request.method == 'POST':
        if get_object_or_none(MedicalInstitutionsType, StakeholderTypeID=request.POST.get('MedicalInstitutionsTypeID')):
            return HttpResponseNotFound("This MedicalInstitutionsType data is already stored")

        hide = True if request.POST.get('hide') == 'on' else False

# Part 2   # Put it as it's
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
        StakeholdersAddress.objects.create(
            national_number=stakeholder,
            address=address
        )


# Part 3
MedicalInstitutionsType.objects.create(
    # MedicalInstitutionsType data
)

# Part 4
return HttpResponse()
