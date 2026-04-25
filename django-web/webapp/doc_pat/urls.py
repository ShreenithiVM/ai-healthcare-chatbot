from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('consultation/', views.create_patient_consultation, name='patient_consultation'),
    path('medical-history/<int:patient_id>/', views.list_medical_documents, name='patient_medical_history'),
    path('api/medical-query/', views.ask_medical_question, name='medical-query'),
]
