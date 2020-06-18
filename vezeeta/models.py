
from cpanel.models import ( PhysicianPatientAppointment ,Physician ,PhysicianClinicWorkingTime,
							Clinic ,PhysicianHospitalWorkingTime ,Hospital,Patient,
							Stakeholders, PhysicianRating,ClinicRating,HospitalRating,MedicalInstitutions,
                            MedicalInstitutionsAddress,MedicalInstitutionsPhone,
                            PhysicianSpecialization,Specialization)
						

from main.utils import get_object_or_none
from django.db import models
from django.contrib.auth.models import User



# booking
class PhysicianPatientBooking(models.Model):

    
    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    ID = models.AutoField(db_column='ID', primary_key=True)
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    booking_date_clinic = models.DateField(db_column='Booking_Date_clinic', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # new
    booking_date_hospital = models.DateField(db_column='Booking_Date_Hospital', blank=True, null=True)
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING, db_column='Clinic_ID')
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, db_column='Hospital_ID')
    phone = models.CharField(db_column='Phone', max_length=25)
    email = models.CharField(db_column='Email', max_length=320, blank=True, null=True)
    message = models.TextField(db_column='Message', blank=True, null=True)
 
    class Meta:
        db_table = 'physician_patient_booking'
        verbose_name = 'Physician Booking'
        verbose_name_plural = 'Physician Bookings'

    def __str__(self):
        return str(self.id)


class ClinicPatientBooking(models.Model):

    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    ID = models.AutoField(db_column='ID', primary_key=True)
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    booking_date_clinic = models.DateField(db_column='Booking_Date_clinic', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # new
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING, db_column='Clinic_ID')
    phone = models.CharField(db_column='Phone', max_length=25)
    email = models.CharField(db_column='Email', max_length=320, blank=True, null=True)
    message = models.TextField(db_column='Message', blank=True, null=True)
 
    class Meta:
        db_table = 'clinic_patient_booking'
        verbose_name = 'Clinic Booking'
        verbose_name_plural = 'Clinic Bookings'

    def __str__(self):
        return str(self.id)


class HospitalPatientBooking(models.Model):

    patient_nn = models.ForeignKey(Patient, models.DO_NOTHING, db_column='Patient_NN')
    ID = models.AutoField(db_column='ID', primary_key=True)
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # new
    booking_date_hospital = models.DateField(db_column='Booking_Date_Hospital', blank=True, null=True)
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, db_column='Hospital_ID')
    phone = models.CharField(db_column='Phone', max_length=25)
    email = models.CharField(db_column='Email', max_length=320, blank=True, null=True)
    message = models.TextField(db_column='Message', blank=True, null=True)
 
    class Meta:
        db_table = 'Hospital_patient_booking'
        verbose_name = 'Hospital Booking'
        verbose_name_plural = 'Hospital Bookings'

    def __str__(self):
        return str(self.id)
        
class PhysicianRecommendation(models.Model) :
    ID = models.AutoField(db_column='ID', primary_key=True)
    physician_nn = models.ForeignKey(Physician, models.DO_NOTHING, db_column='Physician_NN')
    rating = models.IntegerField(db_column='Rating', blank=True,default=3, null=True)
    specialization_id = models.CharField(db_column='Specialization_ID',max_length=50) 
    fee = models.IntegerField(db_column='Fee', blank=True,default=200, null=True)
    booking_count = models.IntegerField(db_column='Booking_Count',default=1, blank=True, null=True)

    class Meta:
        db_table = 'Physician_Recommendation'
        verbose_name = 'Physician Recommendation'
        verbose_name_plural = 'Physician Recommendations'

    def __str__(self):
        return str(self.ID)
