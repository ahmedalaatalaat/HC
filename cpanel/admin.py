from django.contrib import admin
from .models import *
from main.admin import my_admin_site
from jet.filters import DateRangeFilter
from django.contrib.auth.models import User, Group


class InlineStakeholdersPhones(admin.TabularInline):
    model = StakeholdersPhones
    extra = 0


class InlineStakeholdersAddress(admin.TabularInline):
    model = StakeholdersAddress
    extra = 0


class InlinePatientRelativesPhones(admin.TabularInline):
    model = PatientRelativesPhones
    extra = 0


class InlineNurseSpecialization(admin.TabularInline):
    model = NurseSpecialization
    extra = 0


class InlineSpecialistSpecialization(admin.TabularInline):
    model = SpecialistSpecialization
    extra = 0


class InlinePharmacistSpecialization(admin.TabularInline):
    model = PharmacistSpecialization
    extra = 0


class InlineMedicalInstitutionsPhone(admin.TabularInline):
    model = MedicalInstitutionsPhone
    extra = 0


class InlineMedicalInstitutionsAddress(admin.TabularInline):
    model = MedicalInstitutionsAddress
    extra = 0


class InlineLabsAnalysisAndRadiology(admin.TabularInline):
    model = LabsAnalysisAndRadiology
    extra = 0


class InlineInsuranceCompaniesPhone(admin.TabularInline):
    model = InsuranceCompaniesPhone
    extra = 0


class InlineInsuranceCompaniesAddress(admin.TabularInline):
    model = InsuranceCompaniesAddress
    extra = 0


class InlineInsuranceTypes(admin.TabularInline):
    model = InsuranceTypes
    extra = 0


class InlinePhysicianHospitalWorkingTime(admin.TabularInline):
    model = PhysicianHospitalWorkingTime
    extra = 0


class InlinePhysicianClinicWorkingTime(admin.TabularInline):
    model = PhysicianClinicWorkingTime
    extra = 0


class InlinePhysicianRating_For_Physician(admin.TabularInline):
    model = PhysicianRating
    extra = 0
    readonly_fields = ['patient_nn', 'rate', 'patient_comment']

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False


class InlineLabRating_For_Lab(admin.TabularInline):
    model = LabRating
    extra = 0
    readonly_fields = ['patient_nn', 'rate', 'patient_comment']

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False


class InlineClinicRating_For_Clinic(admin.TabularInline):
    model = ClinicRating
    extra = 0
    readonly_fields = ['patient_nn', 'rate', 'patient_comment']

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False


class InlineHospitalRating_For_Hospital(admin.TabularInline):
    model = HospitalRating
    extra = 0
    readonly_fields = ['patient_nn', 'rate', 'patient_comment']

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False


class InlinePhysicianRating_For_Patient(admin.TabularInline):
    model = PhysicianRating
    extra = 0


class InlineLabRating_For_Patient(admin.TabularInline):
    model = LabRating
    extra = 0


class InlineClinicRating_For_Patient(admin.TabularInline):
    model = ClinicRating
    extra = 0


class InlineHospitalRating_For_Patient(admin.TabularInline):
    model = HospitalRating
    extra = 0


class InlineHospitalNurses(admin.TabularInline):
    model = HospitalNurses
    extra = 0


class InlineClinicNurses(admin.TabularInline):
    model = ClinicNurses
    extra = 0


class InlineLabNurses(admin.TabularInline):
    model = LabNurses
    extra = 0


class InlineLabSpecialists(admin.TabularInline):
    model = LabSpecialists
    extra = 0


class InlineHospitalSpecialists(admin.TabularInline):
    model = HospitalSpecialists
    extra = 0


class InlineClinicSpecialists(admin.TabularInline):
    model = ClinicSpecialists
    extra = 0


class InlinePharmacyPharmacists(admin.TabularInline):
    model = PharmacyPharmacists
    extra = 0


class InlinePhysicianSpecialization(admin.TabularInline):
    model = PhysicianSpecialization
    extra = 0


class InlineHospitalSpecialization(admin.TabularInline):
    model = HospitalSpecialization
    extra = 0


class InlineClinicSpecialization(admin.TabularInline):
    model = ClinicSpecialization
    extra = 0


class InlineLabsInsuranceDeals(admin.TabularInline):
    model = LabsInsuranceDeals
    extra = 0


class InlineClinicsInsuranceDeals(admin.TabularInline):
    model = ClinicsInsuranceDeals
    extra = 0


class InlineHospitalInsuranceDeals(admin.TabularInline):
    model = HospitalInsuranceDeals
    extra = 0


class InlinePharmacyInsuranceDeals(admin.TabularInline):
    model = PharmacyInsuranceDeals
    extra = 0


class InlinePatientInsurance(admin.TabularInline):
    model = PatientInsurance
    extra = 0


# ---------------------------------------- Start Admin Models
class Stakeholders_admin(admin.ModelAdmin):
    inlines = [InlineStakeholdersPhones, InlineStakeholdersAddress]
    list_display = ['national_number', 'stakeholder_name', 'stakeholder_last_name', 'gender', 'nationality', 'hide']
    list_filter = [('birthday', DateRangeFilter), 'gender', 'hide', 'stakeholder_type']
    search_fields = ['stakeholder_name', 'national_number', 'stakeholder_type']

    def save_model(self, request, obj, form, change):
        obj.user.is_staff = True
        obj.user.save()
        return super().save_model(request, obj, form, change)


class StakeholdersPhones_admin(admin.ModelAdmin):
    list_display = ['national_number', 'phone']
    search_fields = ['national_number__national_number', 'phone']


class StakeholdersAddress_admin(admin.ModelAdmin):
    list_display = ['national_number', 'address']
    search_fields = ['national_number__national_number', 'address']


class Patient_admin(admin.ModelAdmin):
    inlines = [InlinePatientRelativesPhones, InlinePhysicianRating_For_Patient, InlineLabRating_For_Patient, InlineClinicRating_For_Patient, InlineHospitalRating_For_Patient, InlinePatientInsurance]
    list_display = ['patient_nn', 'patient_name', 'chronic_diseases_name', 'chronic_diseases_type', 'blood_type', 'hide']
    list_filter = [('patient_nn__birthday', DateRangeFilter), 'patient_nn__gender', 'hide']
    search_fields = ['patient_nn__national_number', 'patient_nn__stakeholder_name']

    def patient_name(self, obj):
        if obj.patient_nn.stakeholder_name:
            return f'{obj.patient_nn.stakeholder_name} {obj.patient_nn.stakeholder_last_name}'
        return None

    def save_model(self, request, obj, form, change):
        obj.patient_nn.user.is_staff = True
        group = Group.objects.get(name='Patient')
        group.user_set.add(obj.patient_nn.user)
        obj.patient_nn.user.save()
        return super().save_model(request, obj, form, change)


class PatientRelativesPhones_admin(admin.ModelAdmin):
    list_display = ['patient_nn', 'phone']
    search_fields = ['patient_nn__patient_nn__national_number', 'phone']


class Physician_admin(admin.ModelAdmin):
    inlines = [InlinePhysicianHospitalWorkingTime, InlinePhysicianClinicWorkingTime, InlinePhysicianRating_For_Physician, InlinePhysicianSpecialization]
    list_display = ['physician_nn', 'physician_name', 'rate', 'title', 'hide']
    list_filter = ['title', 'rate', 'hide']
    search_fields = ['physician_nn__national_number', 'physician_nn__stakeholder_name']

    def physician_name(self, obj):
        if obj.physician_nn.stakeholder_name:
            return f'{obj.physician_nn.stakeholder_name} {obj.physician_nn.stakeholder_last_name}'
        return None

    def save_model(self, request, obj, form, change):
        obj.physician_nn.user.is_staff = True
        group = Group.objects.get(name='Physician')
        group.user_set.add(obj.physician_nn.user)
        obj.physician_nn.user.save()
        return super().save_model(request, obj, form, change)


class Nurse_admin(admin.ModelAdmin):
    inlines = [InlineNurseSpecialization]
    list_display = ['nurse_nn', 'nurse_name', 'hide']
    list_filter = ['hide']
    search_fields = ['nurse_nn', 'nurse_nn__stakeholder_name']

    def nurse_name(self, obj):
        return f'{obj.nurse_nn.stakeholder_name} {obj.nurse_nn.stakeholder_last_name}'

    def save_model(self, request, obj, form, change):
        obj.nurse_nn.user.is_staff = True
        group = Group.objects.get(name='Nurse')
        group.user_set.add(obj.nurse_nn.user)
        obj.nurse_nn.user.save()
        return super().save_model(request, obj, form, change)


class NurseSpecialization_admin(admin.ModelAdmin):
    list_display = ['nurse_nn', 'specialization']
    search_fields = ['nurse_nn__nurse_nn__national_number']


class Paramedic_admin(admin.ModelAdmin):
    list_display = ['paramedic_nn', 'paramedic_name', 'ambulance_palte_number', 'hide']
    list_filter = ['hide']
    search_fields = ['paramedic_nn__national_number', 'ambulance_palte_number', 'paramedic_nn__stakeholder_name']

    def paramedic_name(self, obj):
        if obj.paramedic_nn.stakeholder_name:
            return f'{obj.paramedic_nn.stakeholder_name} {obj.paramedic_nn.stakeholder_last_name}'
        return None

    def save_model(self, request, obj, form, change):
        obj.paramedic_nn.user.is_staff = True
        group = Group.objects.get(name='Paramedic')
        group.user_set.add(obj.paramedic_nn.user)
        obj.paramedic_nn.user.save()
        return super().save_model(request, obj, form, change)


class Specialist_admin(admin.ModelAdmin):
    inlines = [InlineSpecialistSpecialization]
    list_display = ['specialist_nn', 'specialist_name', 'hide']
    list_filter = ['hide']
    search_fields = ['specialist_nn__stakeholder_name', 'specialist_nn__national_number']

    def specialist_name(self, obj):
        if obj.specialist_nn.stakeholder_name:
            return f'{obj.specialist_nn.stakeholder_name} {obj.specialist_nn.stakeholder_last_name}'
        return None

    def save_model(self, request, obj, form, change):
        obj.specialist_nn.user.is_staff = True
        group = Group.objects.get(name='Specialist')
        group.user_set.add(obj.specialist_nn.user)
        obj.specialist_nn.user.save()
        return super().save_model(request, obj, form, change)


class SpecialistSpecialization_admin(admin.ModelAdmin):
    list_display = ['specialist_nn', 'specialization']
    search_fields = ['specialist_nn__specialist_nn__national_number', 'specialization']


class Pharmacist_admin(admin.ModelAdmin):
    inlines = [InlinePharmacistSpecialization]
    list_display = ['pharmacist_nn', 'pharmacist_name', 'hide']
    list_filter = ['hide']
    search_fields = ['pharmacist_nn__national_number', 'pharmacist_nn__stakeholder_name']

    def pharmacist_name(self, obj):
        if obj.pharmacist_nn.stakeholder_name:
            return f'{obj.pharmacist_nn.stakeholder_name} {obj.pharmacist_nn.stakeholder_last_name}'
        return None

    def save_model(self, request, obj, form, change):
        obj.pharmacist_nn.user.is_staff = True
        group = Group.objects.get(name='Pharmacist')
        group.user_set.add(obj.pharmacist_nn.user)
        obj.pharmacist_nn.user.save()
        return super().save_model(request, obj, form, change)


class PharmacistSpecialization_admin(admin.ModelAdmin):
    list_display = ['pharmacist_nn', 'specialization']
    search_fields = ['pharmacist_nn__pharmacist_nn__national_number', 'specialization']


class MedicalInstitutions_admin(admin.ModelAdmin):
    inlines = [InlineMedicalInstitutionsPhone, InlineMedicalInstitutionsAddress]
    list_display = ['institution_id', 'institution_name', 'hide']
    list_filter = ['hide']
    search_fields = ['institution_name', 'institution_id']

    def save_model(self, request, obj, form, change):
        obj.user.is_staff = True
        group = Group.objects.get(name='Medical Institution')
        group.user_set.add(obj.user)
        obj.user.save()
        return super().save_model(request, obj, form, change)


class MedicalInstitutionsPhone_admin(admin.ModelAdmin):
    list_display = ['institution', 'medicalInstitutions_name', 'phone']
    search_fields = ['institution__institution_id', 'phone', 'institution__institution_name']

    def medicalInstitutions_name(self, obj):
        if obj.institution.institution_name:
            return obj.institution.institution_name
        return None


class MedicalInstitutionsAddres_admin(admin.ModelAdmin):
    list_display = ['institution', 'medicalInstitutions_name', 'address']
    search_fields = ['institution__institution_id', 'address', 'institution__institution_name']

    def medicalInstitutions_name(self, obj):
        if obj.institution.institution_name:
            return obj.institution.institution_name
        return None


class Labs_admin(admin.ModelAdmin):
    inlines = [InlineLabsAnalysisAndRadiology, InlineLabRating_For_Lab, InlineLabNurses, InlineLabSpecialists, InlineLabsInsuranceDeals]
    list_display = ['lab', 'name', 'email', 'fax', 'hide']
    list_filter = ['hide']
    search_fields = ['lab__institution_id', 'lab__institution_name', 'email', 'fax']

    def save_model(self, request, obj, form, change):
        obj.lab.user.is_staff = True
        group = Group.objects.get(name='Lab')
        group.user_set.add(obj.lab.user)
        obj.lab.user.save()
        return super().save_model(request, obj, form, change)

    def name(self, obj):
        return obj.lab.institution_name


class LabsAnalysisAndRadiology_admin(admin.ModelAdmin):
    list_display = ['lab', 'analysis_and_radiology']
    search_fields = ['lab__lab__institution_id', 'analysis_and_radiology']


class Clinic_admin(admin.ModelAdmin):
    inlines = [InlineClinicRating_For_Clinic, InlineClinicNurses, InlineClinicSpecialists, InlineClinicSpecialization, InlineClinicsInsuranceDeals]
    list_display = ['clinic', 'name', 'email', 'fax', 'er_availability', 'hide']
    list_filter = ['er_availability', 'hide']
    search_fields = ['clinic__institution_id', 'clinic__institution_name', 'email', 'fax']

    def name(self, obj):
        return obj.clinic.institution_name

    def save_model(self, request, obj, form, change):
        obj.clinic.user.is_staff = True
        group = Group.objects.get(name='Clinic')
        group.user_set.add(obj.clinic.user)
        obj.clinic.user.save()
        return super().save_model(request, obj, form, change)


class Pharmacy_admin(admin.ModelAdmin):
    inlines = [InlinePharmacyPharmacists, InlinePharmacyInsuranceDeals]
    list_display = ['pharmacy', 'name', 'pharmacy_type', 'Owner', 'hide']
    list_filter = ['pharmacy_type', 'hide']
    search_fields = ['pharmacy__institution_id', 'pharmacy__institution_name', 'pharmacy_type']

    def save_model(self, request, obj, form, change):
        obj.pharmacy.user.is_staff = True
        group = Group.objects.get(name='Pharmacy')
        group.user_set.add(obj.pharmacy.user)
        obj.pharmacy.user.save()
        return super().save_model(request, obj, form, change)

    def name(self, obj):
        return obj.pharmacy.institution_name

    def Owner(self, obj):
        if obj.owner.pharmacist_nn.stakeholder_name:
            return obj.owner.pharmacist_nn.stakeholder_name
        return obj.owner


class Hospital_admin(admin.ModelAdmin):
    inlines = [InlineHospitalRating_For_Hospital, InlineHospitalNurses, InlineHospitalSpecialists, InlineHospitalSpecialization, InlineHospitalInsuranceDeals]
    list_display = ['hospital', 'name', 'email', 'fax', 'hospital_type', 'manager', 'er_availability', 'hide']
    list_filter = ['hospital_type', 'er_availability', 'hide']
    search_fields = ['hospital__institution_id', 'hospital__institution_name']

    def save_model(self, request, obj, form, change):
        obj.hospital.user.is_staff = True
        group = Group.objects.get(name='Hospital')
        group.user_set.add(obj.hospital.user)
        obj.hospital.user.save()
        return super().save_model(request, obj, form, change)

    def name(self, obj):
        return obj.hospital.institution_name


class InsuranceCompanies_admin(admin.ModelAdmin):
    inlines = [InlineInsuranceCompaniesPhone, InlineInsuranceCompaniesAddress, InlineInsuranceTypes]
    list_display = ['company_id', 'company_name', 'company_type', 'email', 'fax', 'hide']
    list_filter = ['hide', 'company_type']
    search_fields = ['company_id', 'company_name']

    def save_model(self, request, obj, form, change):
        obj.user.is_staff = True
        group = Group.objects.get(name='Insurance Company')
        group.user_set.add(obj.user)
        obj.user.save()
        return super().save_model(request, obj, form, change)


class InsuranceCompaniesPhone_admin(admin.ModelAdmin):
    list_display = ['company', 'insuranceCompanies_name', 'phone']
    search_fields = ['company__company_id', 'phone']

    def insuranceCompanies_name(self, obj):
        return obj.company.company_name


class InsuranceCompaniesAddress_admin(admin.ModelAdmin):
    list_display = ['company', 'insuranceCompanies_name', 'address']
    search_fields = ['company__company_id', 'address']

    def insuranceCompanies_name(self, obj):
        return obj.company.company_name


class InsuranceTypes_admin(admin.ModelAdmin):
    list_display = ['type_id', 'company', 'type_name', 'hide']
    list_filter = ['hide']
    search_fields = ['type_id', 'company', 'type_name']


class Specialization_admin(admin.ModelAdmin):
    list_display = ['specialization_id', 'name', 'hide']
    list_filter = ['hide']
    search_fields = ['specialization_id', 'name']


class PatientHistory_admin(admin.ModelAdmin):
    list_display = ['patient_nn', 'patient_name', 'physician_nn', 'physician_name', 'date_time', 'visitation_type', 'prescription', 'diagnouse', 'disease_priority', 'hide']
    search_fields = ['id', 'patient_nn', 'physician_nn', 'disease_priority']
    list_filter = ['hide', 'disease_priority', ('date_time', DateRangeFilter), 'visitation_type']

    def patient_name(self, obj):
        if obj.patient_nn.patient_nn.stakeholder_name:
            return f'{obj.patient_nn.patient_nn.stakeholder_name} {obj.patient_nn.patient_nn.stakeholder_last_name}'
        return None

    def physician_name(self, obj):
        if obj.physician_nn.physician_nn.stakeholder_name:
            return f'{obj.physician_nn.physician_nn.stakeholder_name} {obj.physician_nn.physician_nn.stakeholder_last_name}'
        return None


class PhysicianPatientAppointment_admin(admin.ModelAdmin):
    list_display = ['patient_nn', 'patient_name', 'physician_nn', 'physician_name', 'date_time', 'place']
    list_filter = [('date_time', DateRangeFilter), 'date_time']
    search_fields = ['patient_nn__patient_nn__national_number', 'physician_nn__physician_nn__national_number']

    def patient_name(self, obj):
        if obj.patient_nn.patient_nn.stakeholder_name:
            return f'{obj.patient_nn.patient_nn.stakeholder_name} {obj.patient_nn.patient_nn.stakeholder_last_name}'
        return None

    def physician_name(self, obj):
        if obj.physician_nn.physician_nn.stakeholder_name:
            return f'{obj.physician_nn.physician_nn.stakeholder_name} {obj.physician_nn.physician_nn.stakeholder_last_name}'
        return None


class PhysicianHospitalWorkingTime_admin(admin.ModelAdmin):
    list_display = ['physician_nn', 'physician_name', 'hospital', 'hospital_name', 'week_day', 'start_time', 'end_time', 'fee', 'hide']
    list_filter = ['start_time', 'end_time', 'hide', 'week_day']
    search_fields = ['physician_nn__physician_nn__national_number', 'hospital__hospital__institution_id']

    def physician_name(self, obj):
        if obj.physician_nn.physician_nn.stakeholder_name:
            return f'{obj.physician_nn.physician_nn.stakeholder_name} {obj.physician_nn.physician_nn.stakeholder_last_name}'
        return None

    def hospital_name(self, obj):
        if obj.hospital.hospital.institution_name:
            return obj.hospital.hospital.institution_name
        return None


class PhysicianClinicWorkingTime_admin(admin.ModelAdmin):
    list_display = ['physician_nn', 'physician_name', 'clinic', 'clinic_name', 'week_day', 'start_time', 'end_time', 'fee', 'hide']
    list_filter = ['start_time', 'end_time', 'hide', 'week_day']
    search_fields = ['physician_nn__physician_nn__national_number', 'clinic__clinic__institution_id']

    def physician_name(self, obj):
        if obj.physician_nn.physician_nn.stakeholder_name:
            return f'{obj.physician_nn.physician_nn.stakeholder_name} {obj.physician_nn.physician_nn.stakeholder_last_name}'
        return None

    def clinic_name(self, obj):
        if obj.clinic.clinic.institution_name:
            return obj.clinic.clinic.institution_name
        return None


class PhysicianRating_admin(admin.ModelAdmin):
    list_display = ['patient_nn', 'patient_name', 'physician_nn', 'physician_name', 'rate', 'Patient_comment']
    list_filter = ['rate']
    search_fields = ['physician_nn__physician_nn__national_number', 'patient_nn__patient_nn__national_number']

    def Patient_comment(self, obj):
        if obj.patient_comment:
            return obj.patient_comment
        return None

    def patient_name(self, obj):
        if obj.patient_nn.patient_nn.stakeholder_name:
            return f'{obj.patient_nn.patient_nn.stakeholder_name} {obj.patient_nn.patient_nn.stakeholder_last_name}'
        return None

    def physician_name(self, obj):
        if obj.physician_nn.physician_nn.stakeholder_name:
            return f'{obj.physician_nn.physician_nn.stakeholder_name} {obj.physician_nn.physician_nn.stakeholder_last_name}'
        return None


class LabRating_admin(admin.ModelAdmin):
    list_display = ['patient_nn', 'patient_name', 'lab', 'lab_name', 'Patient_comment']
    search_fields = ['patient_nn__patient_nn__national_number', 'lab__lab__institution_id']

    def Patient_comment(self, obj):
        if obj.patient_comment:
            return obj.patient_comment
        return None

    def patient_name(self, obj):
        if obj.patient_nn.patient_nn.stakeholder_name:
            return f'{obj.patient_nn.patient_nn.stakeholder_name} {obj.patient_nn.patient_nn.stakeholder_last_name}'
        return None

    def lab_name(self, obj):
        if obj.lab.lab.institution_name:
            return obj.lab.lab.institution_name
        return None


class ClinicRating_admin(admin.ModelAdmin):
    list_display = ['patient_nn', 'patient_name', 'clinic', 'clinic_name', 'Patient_comment']
    search_fields = ['patient_nn__patient_nn__national_number', 'clinic__clinic__institution_id']

    def Patient_comment(self, obj):
        if obj.patient_comment:
            return obj.patient_comment
        return None

    def patient_name(self, obj):
        if obj.patient_nn.patient_nn.stakeholder_name:
            return f'{obj.patient_nn.patient_nn.stakeholder_name} {obj.patient_nn.patient_nn.stakeholder_last_name}'
        return None

    def clinic_name(self, obj):
        if obj.clinic.clinic.institution_name:
            return obj.clinic.clinic.institution_name
        return None


class HospitalRating_admin(admin.ModelAdmin):
    list_display = ['patient_nn', 'patient_name', 'hospital', 'hospital_name', 'Patient_comment']
    search_fields = ['patient_nn__patient_nn__national_number', 'hospital__hospital__institution_id']

    def Patient_comment(self, obj):
        if obj.patient_comment:
            return obj.patient_comment
        return None

    def patient_name(self, obj):
        if obj.patient_nn.patient_nn.stakeholder_name:
            return f'{obj.patient_nn.patient_nn.stakeholder_name} {obj.patient_nn.patient_nn.stakeholder_last_name}'
        return None

    def hospital_name(self, obj):
        if obj.hospital.hospital.institution_name:
            return obj.hospital.hospital.institution_name
        return None


class HospitalNurses_admin(admin.ModelAdmin):
    list_display = ['hospital', 'hospital_name', 'nurse_name', 'nurse_nn']
    search_fields = ['nurse_nn__nurse_nn__national_number', 'hospital__hospital__institution_id']

    def nurse_name(self, obj):
        return f'{obj.nurse_nn.nurse_nn.stakeholder_name} {obj.nurse_nn.nurse_nn.stakeholder_last_name}'

    def hospital_name(self, obj):
        if obj.hospital.hospital.institution_name:
            return obj.hospital.hospital.institution_name
        return None


class ClinicNurses_admin(admin.ModelAdmin):
    list_display = ['clinic', 'clinic_name', 'nurse_nn', 'nurse_name']
    search_fields = ['nurse_nn__nurse_nn__national_number', 'clinic__clinic__institution_id']

    def nurse_name(self, obj):
        return f'{obj.nurse_nn.nurse_nn.stakeholder_name} {obj.nurse_nn.nurse_nn.stakeholder_last_name}'

    def clinic_name(self, obj):
        if obj.clinic.clinic.institution_name:
            return obj.clinic.clinic.institution_name
        return None


class LabNurses_admin(admin.ModelAdmin):
    list_display = ['lab', 'lab_name', 'nurse_nn', 'nurse_name']
    search_fields = ['nurse_nn__nurse_nn__national_number', 'lab__lab__institution_id']

    def nurse_name(self, obj):
        return f'{obj.nurse_nn.nurse_nn.stakeholder_name} {obj.nurse_nn.nurse_nn.stakeholder_last_name}'

    def lab_name(self, obj):
        if obj.lab.lab.institution_name:
            return obj.lab.lab.institution_name
        return None


class LabSpecialists_admin(admin.ModelAdmin):
    list_display = ['lab', 'lab_name', 'specialist_nn', 'specialist_name']
    search_fields = ['lab__lab__institution_id', 'specialist_nn__specialist_nn__national_number']

    def lab_name(self, obj):
        return obj.lab.lab.institution_name

    def specialist_name(self, obj):
        return f'{obj.specialist_nn.specialist_nn.stakeholder_name} {obj.specialist_nn.specialist_nn.stakeholder_last_name}'


class HospitalSpecialists_admin(admin.ModelAdmin):
    list_display = ['hospital', 'hospital_name', 'specialist_nn', 'specialist_name']
    search_fields = ['hospital__hospital__institution_id', 'specialist_nn__specialist_nn__national_number']

    def hospital_name(self, obj):
        return obj.hospital.hospital.institution_name

    def specialist_name(self, obj):
        if obj.specialist_nn.specialist_nn.stakeholder_name:
            return f'{obj.specialist_nn.specialist_nn.stakeholder_name} {obj.specialist_nn.specialist_nn.stakeholder_last_name}'
        return None


class ClinicSpecialists_admin(admin.ModelAdmin):
    list_display = ['clinic', 'clinic_name', 'specialist_nn', 'specialist_name']
    search_fields = ['clinic__clinic__institution_id', 'specialist_nn__specialist_nn__national_number']

    def clinic_name(self, obj):
        return obj.clinic.clinic.institution_name

    def specialist_name(self, obj):
        return f'{obj.specialist_nn.specialist_nn.stakeholder_name} {obj.specialist_nn.specialist_nn.stakeholder_last_name}'


class PharmacyPharmacists_admin(admin.ModelAdmin):
    list_display = ['pharmacy', 'pharmacy_name', 'pharmacist_nn', 'pharmacist_name']
    search_fields = ['pharmacist_nn__pharmacist_nn__national_number', 'pharmacy__pharmacy__institution_id']

    def pharmacy_name(self, obj):
        return obj.pharmacy.pharmacy.institution_name

    def pharmacist_name(self, obj):
        if obj.pharmacist_nn.pharmacist_nn.stakeholder_name:
            if obj.pharmacist_nn.pharmacist_nn.stakeholder_name:
                return f'{obj.pharmacist_nn.pharmacist_nn.stakeholder_name} {obj.pharmacist_nn.pharmacist_nn.stakeholder_last_name}'


class PhysicianSpecialization_admin(admin.ModelAdmin):
    list_display = ['physician_nn', 'physician_name', 'specialization']
    list_filter = ['specialization']
    search_fields = ['physician_nn__physician_nn__national_number']

    def physician_name(self, obj):
        if obj.physician_nn.physician_nn.stakeholder_name:
            return f'{obj.physician_nn.physician_nn.stakeholder_name} {obj.physician_nn.physician_nn.stakeholder_last_name}'
        return None


class HospitalSpecialization_admin(admin.ModelAdmin):
    list_display = ['hospital', 'hospital_name', 'specialization']
    list_filter = ['specialization']
    search_fields = ['hospital__hospital__institution_id']

    def hospital_name(self, obj):
        return obj.hospital.hospital.institution_name


class ClinicSpecialization_admin(admin.ModelAdmin):
    list_display = ['clinic', 'clinic_name', 'specialization']
    list_filter = ['specialization']
    search_fields = ['clinic__clinic__institution_id']

    def clinic_name(self, obj):
        return obj.clinic.clinic.institution_name


class LabsInsuranceDeals_admin(admin.ModelAdmin):
    list_display = ['lab', 'lab_name', 'insurance_type', 'insurance_company', 'insurance_type_name', 'discount']
    search_fields = ['lab__lab__institution_id', 'insurance_type__company__company_id', 'insurance_type__company__company_name']

    def lab_name(self, obj):
        return obj.lab.lab.institution_name

    def insurance_company(self, obj):
        return obj.insurance_type.company.company_name

    def insurance_type_name(self, obj):
        return obj.insurance_type.type_name


class ClinicsInsuranceDeals_admin(admin.ModelAdmin):
    list_display = ['clinic', 'clinic_name', 'insurance_type', 'insurance_company', 'insurance_type_name', 'discount']
    search_fields = ['clinic__clinic__institution_id', 'insurance_type__company__company_id', 'insurance_type__company__company_name']

    def clinic_name(self, obj):
        return obj.clinic.clinic.institution_name

    def insurance_company(self, obj):
        return obj.insurance_type.company.company_name

    def insurance_type_name(self, obj):
        return obj.insurance_type.type_name


class HospitalInsuranceDeals_admin(admin.ModelAdmin):
    list_display = ['hospital', 'hospital_name', 'insurance_type', 'insurance_company', 'insurance_type_name', 'discount']
    search_fields = ['hospital__hospital__institution_id', 'insurance_type__company__company_id', 'insurance_type__company__company_name']

    def hospital_name(self, obj):
        return obj.hospital.hospital.institution_name

    def insurance_company(self, obj):
        return obj.insurance_type.company.company_name

    def insurance_type_name(self, obj):
        return obj.insurance_type.type_name


class PharmacyInsuranceDeals_admin(admin.ModelAdmin):
    list_display = ['pharmacy', 'pharmacy_name', 'insurance_type', 'insurance_company', 'insurance_type_name', 'discount']
    search_fields = ['pharmacy__pharmacy__institution_id', 'insurance_type__company__company_id', 'insurance_type__company__company_name']

    def pharmacy_name(self, obj):
        return obj.pharmacy.pharmacy.institution_name

    def insurance_company(self, obj):
        return obj.insurance_type.company.company_name

    def insurance_type_name(self, obj):
        return obj.insurance_type.type_name


class PatientInsurance_admin(admin.ModelAdmin):
    list_display = ['patient_nn', 'patient_name', 'insurance_company', 'insurance_type']
    search_fields = ['patient_nn__patient_nn__national_number', 'insurance_type__company__company_id', 'insurance_type__company__company_name']

    def patient_name(self, obj):
        return f'{obj.patient_nn.patient_nn.stakeholder_name} {obj.patient_nn.patient_nn.stakeholder_last_name}'

    def insurance_company(self, obj):
        return obj.insurance_type.company.company_name


my_admin_site.register(Stakeholders, Stakeholders_admin)
my_admin_site.register(StakeholdersPhones, StakeholdersPhones_admin)
my_admin_site.register(StakeholdersAddress, StakeholdersAddress_admin)
my_admin_site.register(Patient, Patient_admin)
my_admin_site.register(PatientRelativesPhones, PatientRelativesPhones_admin)
my_admin_site.register(Physician, Physician_admin)
my_admin_site.register(Nurse, Nurse_admin)
my_admin_site.register(NurseSpecialization, NurseSpecialization_admin)
my_admin_site.register(Paramedic, Paramedic_admin)
my_admin_site.register(Specialist, Specialist_admin)
my_admin_site.register(SpecialistSpecialization, SpecialistSpecialization_admin)
my_admin_site.register(Pharmacist, Pharmacist_admin)
my_admin_site.register(PharmacistSpecialization, PharmacistSpecialization_admin)
my_admin_site.register(MedicalInstitutions, MedicalInstitutions_admin)
my_admin_site.register(MedicalInstitutionsPhone, MedicalInstitutionsPhone_admin)
my_admin_site.register(MedicalInstitutionsAddress, MedicalInstitutionsAddres_admin)
my_admin_site.register(Labs, Labs_admin)
my_admin_site.register(LabsAnalysisAndRadiology, LabsAnalysisAndRadiology_admin)
my_admin_site.register(Clinic, Clinic_admin)
my_admin_site.register(Pharmacy, Pharmacy_admin)
my_admin_site.register(Hospital, Hospital_admin)
my_admin_site.register(InsuranceCompanies, InsuranceCompanies_admin)
my_admin_site.register(InsuranceCompaniesPhone, InsuranceCompaniesPhone_admin)
my_admin_site.register(InsuranceCompaniesAddress, InsuranceCompaniesAddress_admin)
my_admin_site.register(InsuranceTypes, InsuranceTypes_admin)
my_admin_site.register(Specialization, Specialization_admin)
my_admin_site.register(PatientHistory, PatientHistory_admin)
my_admin_site.register(PhysicianPatientAppointment, PhysicianPatientAppointment_admin)
my_admin_site.register(PhysicianHospitalWorkingTime, PhysicianHospitalWorkingTime_admin)
my_admin_site.register(PhysicianClinicWorkingTime, PhysicianClinicWorkingTime_admin)
my_admin_site.register(PhysicianRating, PhysicianRating_admin)
my_admin_site.register(LabRating, LabRating_admin)
my_admin_site.register(ClinicRating, ClinicRating_admin)
my_admin_site.register(HospitalRating, HospitalRating_admin)
my_admin_site.register(HospitalNurses, HospitalNurses_admin)
my_admin_site.register(ClinicNurses, ClinicNurses_admin)
my_admin_site.register(LabNurses, LabNurses_admin)
my_admin_site.register(LabSpecialists, LabSpecialists_admin)
my_admin_site.register(HospitalSpecialists, HospitalSpecialists_admin)
my_admin_site.register(ClinicSpecialists, ClinicSpecialists_admin)
my_admin_site.register(PharmacyPharmacists, PharmacyPharmacists_admin)  # ---
my_admin_site.register(PhysicianSpecialization, PhysicianSpecialization_admin)
my_admin_site.register(HospitalSpecialization, HospitalSpecialization_admin)
my_admin_site.register(ClinicSpecialization, ClinicSpecialization_admin)
my_admin_site.register(LabsInsuranceDeals, LabsInsuranceDeals_admin)
my_admin_site.register(ClinicsInsuranceDeals, ClinicsInsuranceDeals_admin)
my_admin_site.register(HospitalInsuranceDeals, HospitalInsuranceDeals_admin)
my_admin_site.register(PharmacyInsuranceDeals, PharmacyInsuranceDeals_admin)
my_admin_site.register(PatientInsurance, PatientInsurance_admin)
