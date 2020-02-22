# In Views
medical_institution = get_object_or_none(MedicalInstitutions, institution_id=request.POST.get('institution_id'))
if not medical_institution:
    # Add User to django
    user = User.objects.create_user(
        username=request.POST.get('institution_id'),
        password=request.POST.get('password')
    )

    # Add user to the group
    group = Group.objects.get(name='MedicalInstitutions')
    group.user_set.add(user)

    medical_institution = MedicalInstitutions.objects.create(
        institution_id=request.POST.get('institution_id'),
        institution_name=request.POST.get('institution_name'),
        user=user
    )

    if request.FILES.get('image'):
        medical_institution.image = request.FILES.get('image')
        medical_institution.save()

else:
    group = Group.objects.get(name='MedicalInstitutions')
    group.user_set.add(medical_institution.user)

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

return HttpResponse()


# In Templates

# Replace All Phone with phones
# Remove the three dots in the header
# Add required and autocomplete='nope'
# Add min="0" to the id field
# Add Password
'''
<div class="col-lg-12 p-t-20">
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
        <input class="mdl-textfield__input" id="txtPwd" type="password" name="password" required/>
        <label class="mdl-textfield__label">
            Password
        </label>
    </div>
</div>
<div class="col-lg-12 p-t-20">
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
        <input class="mdl-textfield__input" id="txtConfirmPwd" type="password" name="password" required/>
        <label class="mdl-textfield__label">
            Confirm Password
        </label>
    </div>
</div>
'''
