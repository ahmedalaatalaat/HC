# --------------------- if stakeholder
# part 1 # Put it as it's
stakeholder = get_object_or_404(Stakeholders, national_number=NN)
stakeholder_numbers = stakeholder.get_phone
stakeholder_address = stakeholder.get_address


# part 2
StakeholderType = get_object_or_404(StakeholderType, StakeholderTypeID=NN)

# part 3
context = {
    'stakeholder': stakeholder,
    'main_phone': stakeholder_numbers[0],
    'phones': stakeholder_numbers[1:],
    'main_address': stakeholder_address[0],
    'address': stakeholder_address[1:],
    'StakeholderType': StakeholderType,
}

# Part 4
return render(request, 'cpanel/StakeholderType/StakeholderType_edit.html', context)

# --------------------- if Medical Institution

# Part 1
institution = get_object_or_404(MedicalInstitutions, institution_id=id)
institution_numbers = MedicalInstitutionsPhone.get_phone
institution_address = MedicalInstitutionsAddress.get_address

# Part 2
MedicalInstitutionType = get_object_or_404(MedicalInstitutionType, MedicalInstitutionTypeID=id)

# Part 3
context = {
    'institution': institution,
    'main_phone': institution_numbers[0],
    'phones': institution_numbers[1:],
    'main_address': institution_address[0],
    'address': institution_address[1:],
    'MedicalInstitutionType': MedicalInstitutionType,
}

# Part 4
return render(request, 'cpanel/MedicalInstitutionType/MedicalInstitutionType_edit.html', context)
