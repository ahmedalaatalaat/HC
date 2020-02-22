# In Template
# Replace Phone with phone
# remove the three dots
# Add password edit
'''
<div class="col-lg-12 p-t-20">
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width" id="password_main_div">
        <input class="mdl-textfield__input" type="password" name="password" />
        <label class="mdl-textfield__label">
            Old Password
        </label>
    </div>
</div>

<div class="col-lg-12 p-t-20">
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
        <input class="mdl-textfield__input" id="txtPwd" type="password" name="password" />
        <label class="mdl-textfield__label">
            Password
        </label>
    </div>
</div>
<div class="col-lg-12 p-t-20">
    <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
        <input class="mdl-textfield__input" id="txtConfirmPwd" type="password" name="password" />
        <label class="mdl-textfield__label">
            Confirm Password
        </label>
    </div>
</div>
'''
# Add reqired and autocomplete="nope"


# In views
# add .phone and .address in context
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

        # MedicalInstitutionType Handle
