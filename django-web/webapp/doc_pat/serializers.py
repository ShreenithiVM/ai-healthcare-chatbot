from rest_framework import serializers
from .models import MedicalProfessional, Patient, MedicalDocument, PatientConsultation

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'user', 'date_of_birth', 'blood_type', 'allergies', 'address', 'phone_number']

class MedicalProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProfessional
        fields = ['id', 'user', 'specialization', 'years_of_experience', 'phone_number']

class MedicalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDocument
        fields = '__all__'

class PatientConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientConsultation
        fields = '__all__'