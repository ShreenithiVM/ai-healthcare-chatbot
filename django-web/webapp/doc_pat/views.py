from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import MedicalProfessional, Patient, MedicalDocument, PatientConsultation
from .serializers import (
    MedicalProfessionalSerializer,
    PatientSerializer,
    MedicalDocumentSerializer,
    PatientConsultationSerializer,
)
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

# Lazy initialization flags
qa_model = None
qa_model_initialized = False

def initialize_qa_model():
    global qa_model, qa_model_initialized
    if not qa_model_initialized:
        # Initialize your QA model here
        print("✅ QA model initialized!")
        qa_model_initialized = True

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    logger.info(f"Incoming registration data: {data}")

    try:
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        )

        role = data.get('role')

        if role == 'patient':
            patient = Patient.objects.create(
                user=user,
                date_of_birth=data.get('date_of_birth'),
                blood_type=data.get('blood_type', ''),
                allergies=data.get('allergies', ''),
                address=data.get('address', ''),
                phone_number=data.get('phone_number', '')
            )
            patient.save()
            logger.info(f"Patient created: {patient}")

        elif role == 'medical_professional':
            professional = MedicalProfessional.objects.create(
                user=user,
                specialization=data.get('specialization'),
                years_of_experience=data.get('years_of_experience'),
                phone_number=data.get('phone_number', '')
            )
            professional.save()
            logger.info(f"Medical professional created: {professional}")

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


    except IntegrityError as e:
        if 'auth_user_username_key' in str(e):
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        elif 'auth_user_email_key' in str(e):
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'A database error occurred.'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return Response({'error': 'Something went wrong. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key, 'message': 'Login successful!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_patient_consultation(request):
    serializer = PatientConsultationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_medical_documents(request, patient_id):
    documents = MedicalDocument.objects.filter(patient_id=patient_id)
    serializer = MedicalDocumentSerializer(documents, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ask_medical_question(request):
    initialize_qa_model()

    question = request.data.get('question')
    if not question:
        return Response({'error': 'Please provide a question.'}, status=status.HTTP_400_BAD_REQUEST)

    # Here you can process the question with your model
    answer = f"Sample answer to: {question}"

    return Response({'answer': answer})