from django.db import models
from main.utils import get_object_or_none

# Enumeration Values
Gender = [('Male', 'Male'), ('Female', 'Female')]

Stakeholder_Type = [('Admin', 'Admin'), ('Patient', 'Patient'), ('Physician', 'Physician'), ('Nurse', 'Nurse'), ('Paramedic', 'Paramedic'), ('Pharmist', 'Pharmist'), ('Specialist', 'Specialist'), ('Clerk', 'Clerk'), ('Editors', 'Editors')]

Marital_Status = [('Single', 'Single'), ('Married', 'Married'), ('Widow', 'Widow'), ('Divorced', 'Divorced')]

Blood_Type = [('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')]

Physician_Title = [("Professor", "Professor"), ("Lecturer", "Lecturer"), ("Consultant", "Consultant"), ("Specialist", "Specialist")]

Patient_Visitation_Type = [('Normal', 'Normal'), ('Consultation', 'Consultation'), ('Operation', 'Operation'), ('ER', 'ER')]

Patient_Disease_Priority = [('Very High', 'Very High'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]

Week_Day = [("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"), ("Thursday", "Thursday"), ("Friday", "Friday"), ("Saturday", "Saturday"), ("Sunday", "Sunday")]
# -- ** StakeHolders And Related Tables ** --


class Stakeholders(models.Model):
    national_number = models.CharField(max_length=20, db_column='National_Number', primary_key=True)
    stakeholder_name = models.CharField(db_column='Stakeholder_Name', max_length=255, blank=True, null=True)
    stakeholder_last_name = models.CharField(db_column='Stakeholder_Last_Name', max_length=255, blank=True, null=True)
    password = models.CharField(db_column='Password', max_length=50, blank=True, null=True)
    birthday = models.DateField(db_column='Birthday', blank=True, null=True)
    gender = models.CharField(db_column='Gender', max_length=6, blank=True, null=True, choices=Gender)
    stakeholder_type = models.CharField(db_column='Stakeholder_Type', max_length=10, blank=True, null=True, choices=Stakeholder_Type)
    email = models.CharField(db_column='Email', max_length=320, blank=True, null=True)
    marital_status = models.CharField(db_column='Marital_Status', max_length=8, blank=True, null=True, choices=Marital_Status)
    image = models.ImageField(default=None, upload_to='Stakeholder/images', db_column='Image', blank=True, null=True)  # new
    nationality = models.CharField(db_column='Nationality', max_length=255, blank=True, null=True)
    cv = models.CharField(db_column='cv', max_length=500, blank=True, null=True)  # new
    created_at = models.DateTimeField(auto_now_add=True)  # new
    updated_at = models.DateTimeField(auto_now=True)  # new
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'stakeholders'
        verbose_name = 'Stakeholder'
        verbose_name_plural = 'Stakeholders'

    def __str__(self):
        return str(self.national_number)

    @property
    def get_phone(self):
        return StakeholdersPhones.objects.filter(national_number=self.national_number)

    @property
    def get_address(self):
        return StakeholdersAddress.objects.filter(national_number=self.national_number)


class StakeholdersPhones(models.Model):
    national_number = models.ForeignKey(Stakeholders, models.DO_NOTHING, db_column='National_Number')
    phone = models.CharField(db_column='Phone', max_length=25)

    class Meta:
        db_table = 'stakeholders_phones'
        unique_together = (('national_number', 'phone'),)
        verbose_name = 'Stakeholders Phone'
        verbose_name_plural = 'Stakeholders Phones'

    def __str__(self):
        return str(self.national_number)


class StakeholdersAddress(models.Model):
    national_number = models.ForeignKey(Stakeholders, models.DO_NOTHING, db_column='National_Number')
    address = models.CharField(db_column='Address', max_length=360)

    class Meta:
        db_table = 'stakeholders_address'
        unique_together = (('national_number', 'address'),)
        verbose_name = 'Stakeholders Address'
        verbose_name_plural = 'Stakeholders Addresses'

    def __str__(self):
        return str(self.national_number)


class Patient(models.Model):
    patient_nn = models.OneToOneField('Stakeholders', models.DO_NOTHING, db_column='Patient_NN', primary_key=True)
    chronic_diseases_name = models.CharField(db_column='Chronic_Diseases_Name', max_length=255, blank=True, null=True)
    chronic_diseases_type = models.CharField(db_column='Chronic_Diseases_Type', max_length=255, blank=True, null=True)
    blood_type = models.CharField(db_column='Blood_Type', max_length=3, blank=True, null=True, choices=Blood_Type)

    class Meta:
        db_table = 'patient'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return (self.patient_nn)

    @property
    def get_phone(self):
        return StakeholdersPhones.objects.filter(national_number=self.patient_nn)

    @property
    def get_address(self):
        return StakeholdersAddress.objects.filter(national_number=self.patient_nn)

    @property
    def get_PatientRelativesPhones(self):
        patient = get_object_or_none(Patient, patient_nn=self.patient_nn)
        return PatientRelativesPhones.objects.filter(patient_nn=patient)


class PatientRelativesPhones(models.Model):
    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    phone = models.CharField(db_column='Phone', max_length=25)

    class Meta:
        db_table = 'patient_relatives_phones'
        unique_together = (('patient_nn', 'phone'),)
        verbose_name = 'Patient Relatives Phone'
        verbose_name_plural = 'Patient Relatives Phones'

    def __str__(self):
        return self.patient_nn


class Physician(models.Model):
    physician_nn = models.OneToOneField('Stakeholders', models.DO_NOTHING, db_column='Physician_NN', primary_key=True)
    rate = models.FloatField(db_column='Rate', blank=True, null=True)
    title = models.CharField(db_column='Title', max_length=10, blank=True, null=True, choices=Physician_Title)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'physician'
        verbose_name = 'Physician'
        verbose_name_plural = 'Physicians'

    def __str__(self):
        return str(self.physician_nn)

    @property
    def get_phone(self):
        return StakeholdersPhones.objects.filter(national_number=self.physician_nn)

    @property
    def get_address(self):
        return StakeholdersAddress.objects.filter(national_number=self.physician_nn)

    @property
    def get_Specialization(self):
        physician = get_object_or_none(Physician, physician_nn=self.physician_nn)
        return PhysicianSpecialization.objects.filter(physician_nn=physician)


class Nurse(models.Model):
    nurse_nn = models.OneToOneField('Stakeholders', models.DO_NOTHING, db_column='Nurse_NN', primary_key=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'nurse'
        verbose_name = 'Nurse'
        verbose_name_plural = 'Nurses'

    def __str__(self):
        return str(self.nurse_nn)

    @property
    def get_Specialization(self):
        x = Nurse.objects.get(pk=self.nurse_nn)
        x._state.db
        return NurseSpecialization.objects.filter(nurse_nn=x)

    @property
    def get_phone(self):
        return StakeholdersPhones.objects.filter(national_number=self.nurse_nn)

    @property
    def get_address(self):
        return StakeholdersAddress.objects.filter(national_number=self.nurse_nn)


class NurseSpecialization(models.Model):
    nurse_nn = models.ForeignKey(Nurse, models.DO_NOTHING, db_column='Nurse_NN')
    specialization = models.CharField(db_column='Specialization', max_length=120)

    class Meta:
        db_table = 'nurse_specialization'
        unique_together = (('nurse_nn', 'specialization'),)
        verbose_name = 'Nurse Specialization'
        verbose_name_plural = 'Nurse Specializations'

    def __str__(self):
        return str(self.nurse_nn)


class Paramedic(models.Model):
    paramedic_nn = models.OneToOneField('Stakeholders', models.DO_NOTHING, db_column='Paramedic_NN', primary_key=True)
    ambulance_palte_number = models.CharField(db_column='Ambulance_Palte_number', max_length=12, blank=True, null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'paramedic'
        verbose_name = 'Paramedic'
        verbose_name_plural = 'Paramedics'

    def __str__(self):
        return self.paramedic_nn

    @property
    def get_phone(self):
        return StakeholdersPhones.objects.filter(national_number=self.paramedic_nn)

    @property
    def get_address(self):
        return StakeholdersAddress.objects.filter(national_number=self.paramedic_nn)


class Specialist(models.Model):
    specialist_nn = models.OneToOneField('Stakeholders', models.DO_NOTHING, db_column='Specialist_NN', primary_key=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'specialist'
        verbose_name = 'Specialist'
        verbose_name_plural = 'Specialists'

    def __str__(self):
        return self.specialist_nn

    @property
    def get_Specialization(self):
        x = Specialist.objects.get(pk=self.specialist_nn)
        x._state.db
        return SpecialistSpecialization.objects.filter(specialist_nn=x)

    @property
    def get_phone(self):
        return StakeholdersPhones.objects.filter(national_number=self.specialist_nn)

    @property
    def get_address(self):
        return StakeholdersAddress.objects.filter(national_number=self.specialist_nn)


class SpecialistSpecialization(models.Model):
    specialist_nn = models.ForeignKey(Specialist, models.DO_NOTHING, db_column='Specialist_NN')
    specialization = models.CharField(db_column='Specialization', max_length=120)

    class Meta:
        db_table = 'specialist_specialization'
        unique_together = (('specialist_nn', 'specialization'),)
        verbose_name = 'Specialist Specialization'
        verbose_name_plural = 'Specialist Specializations'

    def __str__(self):
        return self.specialist_nn


class Pharmacist(models.Model):
    pharmacist_nn = models.OneToOneField('Stakeholders', models.DO_NOTHING, db_column='Pharmacist_NN', primary_key=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'pharmacist'
        verbose_name = 'Pharmacist'
        verbose_name_plural = 'Pharmacists'

    def __str__(self):
        return self.pharmacist_nn

    def get_phone(self):
        return StakeholdersPhones.objects.filter(national_number=self.pharmacist_nn)

    def get_address(self):
        return StakeholdersAddress.objects.filter(national_number=self.pharmacist_nn)

    @property
    def get_Specialization(self):
        x = Pharmacist.objects.get(pk=self.pharmacist_nn)
        x._state.db
        return PharmacistSpecialization.objects.filter(pharmacist_nn=x)


class PharmacistSpecialization(models.Model):
    pharmacist_nn = models.ForeignKey(Pharmacist, models.DO_NOTHING, db_column='Pharmacist_NN')
    specialization = models.CharField(db_column='Specialization', max_length=120)

    class Meta:
        db_table = 'pharmacist_specialization'
        unique_together = (('pharmacist_nn', 'specialization'),)
        verbose_name = 'Pharmacist Specialization'
        verbose_name_plural = 'Pharmacist Specializations'

    def __str__(self):
        return self.pharmacist_nn


# -- ** Medical Institutions And Related Tables ** --

class MedicalInstitutions(models.Model):
    institution_id = models.IntegerField(db_column='ID', primary_key=True)
    image = models.ImageField(upload_to='Medical_Institutions/images', db_column='Image', blank=True, null=True)
    institution_name = models.CharField(db_column='Institution_Name', max_length=120, blank=True, null=True)
    hide = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # new
    updated_at = models.DateTimeField(auto_now=True)  # new

    class Meta:
        db_table = 'medical_institutions'
        verbose_name = 'Medical Institution'
        verbose_name_plural = 'Medical Institutions'

    def __str__(self):
        return str(self.institution_id)

    @property
    def get_phone(self):
        return MedicalInstitutionsPhone.objects.filter(institution=self.institution_id)

    @property
    def get_address(self):
        return MedicalInstitutionsAdress.objects.filter(institution=self.institution_id)


class MedicalInstitutionsPhone(models.Model):
    institution = models.ForeignKey(MedicalInstitutions, models.DO_NOTHING, db_column='Institution_ID')
    phone = models.CharField(db_column='Phone', max_length=25)

    class Meta:
        db_table = 'medical_institutions_phone'
        unique_together = (('institution', 'phone'),)
        verbose_name = 'Medical Institution Phone'
        verbose_name_plural = 'Medical Institution Phones'

    def __str__(self):
        return self.institution


class MedicalInstitutionsAdress(models.Model):
    institution = models.ForeignKey(MedicalInstitutions, models.DO_NOTHING, db_column='Institution_ID')
    address = models.CharField(db_column='Adress', max_length=360)

    class Meta:
        db_table = 'medical_institutions_adress'
        unique_together = (('institution', 'address'),)
        verbose_name = 'Medical Institution Address'
        verbose_name_plural = 'Medical Institution Addresses'

    def __str__(self):
        return self.institution


class Labs(models.Model):
    lab = models.OneToOneField('MedicalInstitutions', models.DO_NOTHING, db_column='Lab_ID', primary_key=True)
    email = models.CharField(max_length=320, blank=True, null=True)
    fax = models.CharField(db_column='Fax', max_length=25, blank=True, null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'labs'
        verbose_name = 'Lab'
        verbose_name_plural = 'Labs'

    def __str__(self):
        return self.lab

    @property
    def get_phone(self):
        return MedicalInstitutionsPhone.objects.filter(institution=self.lab)

    @property
    def get_address(self):
        return MedicalInstitutionsAdress.objects.filter(institution=self.lab)

    @property
    def get_A_R(self):
        x = Labs.objects.get(pk=self.lab)
        x._state.db
        return LabsAnalysisAndRadiology.objects.filter(lab=x)


class LabsAnalysisAndRadiology(models.Model):
    lab = models.ForeignKey(Labs, models.DO_NOTHING, db_column='Lab_ID')
    analysis_and_radiology = models.CharField(db_column='Analysis_And_Radiology', max_length=25)

    class Meta:
        db_table = 'labs_analysis_and_radiology'
        unique_together = (('lab', 'analysis_and_radiology'),)
        verbose_name = 'Lab Analysis And Radiology'
        verbose_name_plural = 'Labs Analysis And Radiology'

    def __str__(self):
        return self.lab


class Clinic(models.Model):
    clinic = models.OneToOneField('MedicalInstitutions', models.DO_NOTHING, db_column='Clinic_ID', primary_key=True)
    email = models.CharField(max_length=320, blank=True, null=True)
    fax = models.CharField(db_column='Fax', max_length=25, blank=True, null=True)
    er_availability = models.BooleanField(db_column='ER_Availability', blank=True, null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'clinic'
        verbose_name = 'Clinic'
        verbose_name_plural = 'Clinics'

    def __str__(self):
        return str(self.clinic)

    @property
    def get_phone(self):
        return MedicalInstitutionsPhone.objects.filter(institution=self.clinic)

    @property
    def get_address(self):
        return MedicalInstitutionsAdress.objects.filter(institution=self.clinic)


class Pharmacy(models.Model):
    pharmacy = models.OneToOneField(MedicalInstitutions, models.DO_NOTHING, db_column='Pharmacy_ID', primary_key=True)
    pharmacy_type = models.CharField(db_column='Pharmacy_Type', max_length=120, blank=True, null=True)
    owner = models.ForeignKey(Pharmacist, models.DO_NOTHING, db_column='Owner')
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'pharmacy'
        verbose_name = 'Pharmacy'
        verbose_name_plural = 'Pharmacies'

    @property
    def get_phone(self):
        return MedicalInstitutionsPhone.objects.filter(institution=self.pharmacy)

    @property
    def get_address(self):
        return MedicalInstitutionsAdress.objects.filter(institution=self.pharmacy)

    def __str__(self):
        return str(self.pharmacy)


class Hospital(models.Model):
    hospital = models.OneToOneField('MedicalInstitutions', models.DO_NOTHING, db_column='Hospital_ID', primary_key=True)
    email = models.CharField(db_column='Email', max_length=320, blank=True, null=True)
    fax = models.CharField(db_column='Fax', max_length=25, blank=True, null=True)
    er_availability = models.BooleanField(db_column='ER_Availability', blank=True, null=True)
    hospital_type = models.CharField(db_column='Hospital_type', max_length=120, blank=True, null=True)
    manager = models.CharField(max_length=60, blank=True, null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'hospital'
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitals'

    @property
    def get_phone(self):
        return MedicalInstitutionsPhone.objects.filter(institution=self.hospital)

    @property
    def get_address(self):
        return MedicalInstitutionsAdress.objects.filter(institution=self.hospital)

    def __str__(self):
        return str(self.hospital)

# -- ** Insurance Tables ** --


class InsuranceCompanies(models.Model):
    company_id = models.IntegerField(db_column='ID', primary_key=True)
    email = models.CharField(db_column='Email', max_length=320, blank=True, null=True)
    fax = models.CharField(db_column='Fax', max_length=25, blank=True, null=True)
    company_name = models.CharField(db_column='Company_Name', max_length=120, blank=True, null=True)
    company_type = models.CharField(db_column='Company_Type', max_length=120, blank=True, null=True)
    hide = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # new
    updated_at = models.DateTimeField(auto_now=True)  # new

    class Meta:
        db_table = 'insurance_companies'
        verbose_name = 'Insurance Company'
        verbose_name_plural = 'Insurance Companies'

    def __str__(self):
        return self.company_id

    @property
    def get_phone(self):
        return InsuranceCompaniesPhone.objects.filter(company=self.company_id)

    @property
    def get_address(self):
        return InsuranceCompaniesAddress.objects.filter(company=self.company_id)


class InsuranceCompaniesPhone(models.Model):
    company = models.ForeignKey(InsuranceCompanies, models.DO_NOTHING, db_column='Company_ID')
    phone = models.CharField(db_column='Phone', max_length=25)

    class Meta:
        db_table = 'insurance_companies_phone'
        unique_together = (('company', 'phone'),)
        verbose_name = 'Insurance Company Phone'
        verbose_name_plural = 'Insurance Company Phones'

    def __str__(self):
        return self.company


class InsuranceCompaniesAddress(models.Model):
    company = models.ForeignKey(InsuranceCompanies, models.DO_NOTHING, db_column='Company_ID')
    address = models.CharField(db_column='Address', max_length=360)

    class Meta:
        db_table = 'insurance_companies_address'
        unique_together = (('company', 'address'),)
        verbose_name = 'Insurance Company Address'
        verbose_name_plural = 'Insurance Company Addresses'

    def __str__(self):
        return self.company


class InsuranceTypes(models.Model):
    type_id = models.AutoField(db_column='Type_ID', primary_key=True)
    company = models.ForeignKey(InsuranceCompanies, models.DO_NOTHING, db_column='Company_ID')
    type_name = models.CharField(db_column='Type_Name', max_length=120, blank=True, null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'insurance_types'
        unique_together = (('type_name', 'company'),)
        verbose_name = 'Insurance Type'
        verbose_name_plural = 'Insurance Types'

    def __str__(self):
        return self.type_id


# -- ** Other Tables ** --

class Specialization(models.Model):
    specialization_id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'specialization'
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'

    def __str__(self):
        return str(self.specialization_id)


# -- ** Associated Tables ** --

class PatientHistory(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    date_time = models.DateTimeField(db_column='Date_Time')
    visitation_type = models.CharField(db_column='Visitation_Type', max_length=12, blank=True, null=True, choices=Patient_Visitation_Type)
    prescription = models.TextField(db_column='Prescription', blank=True, null=True)
    physician_comments = models.TextField(db_column='Physician_Comments', blank=True, null=True)
    diagnouse = models.CharField(db_column='Diagnouse', max_length=360, blank=True, null=True)
    analysis_radiology = models.CharField(db_column='Analysis_Radiology', max_length=360, blank=True, null=True)
    disease_priority = models.CharField(db_column='Disease_Priority', max_length=9, blank=True, null=True, choices=Patient_Disease_Priority)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'patient_history'
        unique_together = (('patient_nn', 'physician_nn', 'date_time'),)
        verbose_name = 'Patient History'
        verbose_name_plural = 'Patients History'

    def __str__(self):
        return str(self.patient_nn)


class PhysicianPatientAppointment(models.Model):
    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    date_time = models.DateTimeField(db_column='Date_Time')
    place = models.CharField(db_column='Place', max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'physician_patient_appointment'
        unique_together = (('patient_nn', 'physician_nn', 'date_time'),)
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

    def __str__(self):
        return f'Patient:{self.patient_nn}, Physician:{self.physician_nn}'


class PhysicianHospitalWorkingTime(models.Model):
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, db_column='Hospital_ID')
    week_day = models.CharField(db_column='Week_Day', max_length=9, choices=Week_Day)
    start_time = models.TimeField(db_column='Start_Time')
    end_time = models.TimeField(db_column='End_Time')
    fee = models.IntegerField(db_column='Fee', blank=True, null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'physician_hospital_working_time'
        unique_together = (('physician_nn', 'hospital', 'week_day', 'start_time', 'end_time'),)
        verbose_name = 'Physician Hospital Working Time'
        verbose_name_plural = 'Physician Hospital Working Times'

    def __str__(self):
        return self.physician_nn


class PhysicianClinicWorkingTime(models.Model):
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING, db_column='Clinic_ID')
    week_day = models.CharField(db_column='Week_Day', max_length=9, choices=Week_Day)
    start_time = models.TimeField(db_column='Start_Time')
    end_time = models.TimeField(db_column='End_Time')
    fee = models.IntegerField(db_column='Fee', blank=True, null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'physician_clinic_working_time'
        unique_together = (('physician_nn', 'clinic', 'week_day', 'start_time', 'end_time'),)
        verbose_name = 'Physician Clinic Working Time'
        verbose_name_plural = 'Physician Clinic Working Times'

    def __str__(self):
        return str(self.physician_nn)


# -- ** Many-To-Many Relation Tables ** --

# -- ## Rating Relation ##
class PhysicianRating(models.Model):
    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    patient_comment = models.TextField(db_column='Patient_comment', blank=True, null=True)

    class Meta:
        db_table = 'physician_rating'
        unique_together = (('patient_nn', 'physician_nn'),)
        verbose_name = 'Physician Rating'
        verbose_name_plural = 'Physician Ratings'

    def __str__(self):
        return self.physician_nn


class LabRating(models.Model):
    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    lab = models.ForeignKey(Labs, models.DO_NOTHING, db_column='Lab_ID')
    patient_comment = models.TextField(db_column='Patient_comment', blank=True, null=True)

    class Meta:
        db_table = 'lab_rating'
        unique_together = (('patient_nn', 'lab'),)
        verbose_name = 'Lab Rating'
        verbose_name_plural = 'Lab Ratings'

    def __str__(self):
        return self.lab


class ClinicRating(models.Model):
    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING, db_column='Clinic_ID')
    patient_comment = models.TextField(db_column='Patient_comment', blank=True, null=True)

    class Meta:
        db_table = 'clinic_rating'
        unique_together = (('patient_nn', 'clinic'),)
        verbose_name = 'Clinic Rating'
        verbose_name_plural = 'Clinic Ratings'

    def __str__(self):
        return self.clinic


class HospitalRating(models.Model):
    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, db_column='Hospital_ID')
    patient_comment = models.TextField(db_column='Patient_comment', blank=True, null=True)

    class Meta:
        db_table = 'hospital_rating'
        unique_together = (('patient_nn', 'hospital'),)
        verbose_name = 'Hospital Rating'
        verbose_name_plural = 'Hospital Ratings'

    def __str__(self):
        return self.hospital


# -- ## Working Relation ##
# -- Nurses
class HospitalNurses(models.Model):
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, db_column='Hospital_ID')
    nurse_nn = models.ForeignKey(Nurse, models.DO_NOTHING, db_column='Nurse_NN')

    class Meta:
        db_table = 'hospital_nurses'
        unique_together = (('hospital', 'nurse_nn'),)
        verbose_name = 'Hospital Nurse'
        verbose_name_plural = 'Hospital Nurses'

    def __str__(self):
        return f'Nurse:{self.nurse_nn} works in {self.hospital}'


class ClinicNurses(models.Model):
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING, db_column='Clinic_ID')
    nurse_nn = models.ForeignKey(Nurse, models.DO_NOTHING, db_column='Nurse_NN')

    class Meta:
        db_table = 'clinic_nurses'
        unique_together = (('clinic', 'nurse_nn'),)
        verbose_name = 'Clinic Nurse'
        verbose_name_plural = 'Clinic Nurses'

    def __str__(self):
        return f'Nurse:{self.nurse_nn} works in {self.clinic}'


class LabNurses(models.Model):
    lab = models.ForeignKey(Labs, models.DO_NOTHING, db_column='Lab_ID')
    nurse_nn = models.ForeignKey(Nurse, models.DO_NOTHING, db_column='Nurse_NN')

    class Meta:
        db_table = 'lab_nurses'
        unique_together = (('lab', 'nurse_nn'),)
        verbose_name = 'Lab Nurse'
        verbose_name_plural = 'Lab Nurses'

    def __str__(self):
        return f'Nurse:{self.nurse_nn} works in {self.Lab}'


# -- Specialists
class LabSpecialists(models.Model):
    lab = models.ForeignKey(Labs, models.DO_NOTHING, db_column='Lab_ID')
    specialist_nn = models.ForeignKey(Specialist, models.DO_NOTHING, db_column='Specialist_NN')

    class Meta:
        db_table = 'lab_specialists'
        unique_together = (('lab', 'specialist_nn'),)
        verbose_name = 'Lab Specialist'
        verbose_name_plural = 'Lab Specialists'

    def __str__(self):
        return f'Specialist:{self.specialist_nn} works in {self.lab}'


class HospitalSpecialists(models.Model):
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, db_column='Hospital_ID')
    specialist_nn = models.ForeignKey(Specialist, models.DO_NOTHING, db_column='Specialist_NN')

    class Meta:
        db_table = 'hospital_specialists'
        unique_together = (('hospital', 'specialist_nn'),)
        verbose_name = 'Hospital Specialist'
        verbose_name_plural = 'Hospital Specialists'

    def __str__(self):
        return f'Specialist:{self.specialist_nn} works in {self.hospital}'


class ClinicSpecialists(models.Model):
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING, db_column='Clinic_ID')
    specialist_nn = models.ForeignKey(Specialist, models.DO_NOTHING, db_column='Specialist_NN')

    class Meta:
        db_table = 'clinic_specialists'
        unique_together = (('clinic', 'specialist_nn'),)
        verbose_name = 'Clinic Specialist'
        verbose_name_plural = 'Clinic Specialists'

    def __str__(self):
        return f'Specialist:{self.specialist_nn} works in {self.clinic}'


# -- Pharmacists

class PharmacyPharmacists(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, models.DO_NOTHING, db_column='Pharmacy_ID')
    pharmacist_nn = models.ForeignKey(Pharmacist, models.DO_NOTHING, db_column='Pharmacist_NN')

    class Meta:
        db_table = 'pharmacy_pharmacists'
        unique_together = (('pharmacy', 'pharmacist_nn'),)
        verbose_name = 'Pharmacy Specialist'
        verbose_name_plural = 'Pharmacy Specialists'

    def __str__(self):
        return f'Specialist:{self.specialist_nn} works in {self.pharmacy}'

# -- ## Specialization Relations ##


class PhysicianSpecialization(models.Model):
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    specialization = models.ForeignKey(Specialization, models.DO_NOTHING, db_column='Specialization_ID')

    class Meta:
        db_table = 'physician_specialization'
        unique_together = (('physician_nn', 'specialization'),)
        verbose_name = 'Physician Specialization'
        verbose_name_plural = 'Physician Specializations'

    def __str__(self):
        return str(self.physician_nn)

    def get_value(self):
        return self.specialization.name


class HospitalSpecialization(models.Model):
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, db_column='Hospital_ID')
    specialization = models.ForeignKey(Specialization, models.DO_NOTHING, db_column='Specialization_ID')

    class Meta:
        db_table = 'hospital_specialization'
        unique_together = (('hospital', 'specialization'),)
        verbose_name = 'Hospital Specialization'
        verbose_name_plural = 'Hospital Specializations'

    def __str__(self):
        return self.hospital


class ClinicSpecialization(models.Model):
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING, db_column='Clinic_ID')
    specialization = models.ForeignKey(Specialization, models.DO_NOTHING, db_column='Specialization_ID')

    class Meta:
        db_table = 'clinic_specialization'
        unique_together = (('clinic', 'specialization'),)
        verbose_name = 'Clinic Specialization'
        verbose_name_plural = 'Clinic Specializations'

    def __str__(self):
        return self.clinic


# -- ## Insurance Deals Relations ##
class LabsInsuranceDeals(models.Model):
    lab = models.ForeignKey(Labs, models.DO_NOTHING, db_column='Lab_ID')
    insurance_type = models.ForeignKey(InsuranceTypes, models.DO_NOTHING, db_column='Insurance_Type_ID')
    discount = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'labs_insurance_deals'
        unique_together = (('lab', 'insurance_type'),)
        verbose_name = 'Lab Insurance Deal'
        verbose_name_plural = 'Labs Insurance Deals'

    def __str__(self):
        return self.lab


class ClinicsInsuranceDeals(models.Model):
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING, db_column='Clinic_ID')
    insurance_type = models.ForeignKey(InsuranceTypes, models.DO_NOTHING, db_column='Insurance_Type_ID')
    discount = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'clinics_insurance_deals'
        unique_together = (('clinic', 'insurance_type'),)
        verbose_name = 'Clinic Insurance Deal'
        verbose_name_plural = 'Clinics Insurance Deals'

    def __str__(self):
        return self.clinic


class HospitalInsuranceDeals(models.Model):
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, db_column='Hospital_ID')
    insurance_type = models.ForeignKey(InsuranceTypes, models.DO_NOTHING, db_column='Insurance_Type_ID')
    discount = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'hospital_insurance_deals'
        unique_together = (('hospital', 'insurance_type'),)
        verbose_name = 'Hospital Insurance Deal'
        verbose_name_plural = 'Hospitals Insurance Deals'

    def __str__(self):
        return self.hospital


class PharmacyInsuranceDeals(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, models.DO_NOTHING, db_column='Pharmacy_ID')
    insurance_type = models.ForeignKey(InsuranceTypes, models.DO_NOTHING, db_column='Insurance_Type_ID')
    discount = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'pharmacy_insurance_deals'
        unique_together = (('pharmacy', 'insurance_type'),)
        verbose_name = 'Pharmacy Insurance Deal'
        verbose_name_plural = 'Pharmacies Insurance Deals'

    def __str__(self):
        return self.pharmacy


# -- ## Other Relations ##

class PatientInsurance(models.Model):
    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    insurance_type_id = models.IntegerField(db_column='Insurance_Type_ID')

    class Meta:
        db_table = 'patient_insurance'
        unique_together = (('patient_nn', 'insurance_type_id'),)
        verbose_name = 'Patient Insurance'
        verbose_name_plural = 'Patient Insurances'

    def __str__(self):
        return self.patient_nn
