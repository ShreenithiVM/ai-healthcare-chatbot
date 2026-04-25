from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class MedicalProfessional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    years_of_experience = models.IntegerField(null=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class MedicalDocument(models.Model):
    DOCUMENT_TYPES = (
        ('RX', 'Prescription'),
        ('MR', 'Medical Report'),
        ('LR', 'Lab Result'),
        ('NT', 'Doctor Notes')
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    document_type = models.CharField(max_length=2, choices=DOCUMENT_TYPES)
    upload_date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(MedicalProfessional, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'medical_documents'

class PatientConsultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(MedicalProfessional, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    consultation_date = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'patient_consultations'