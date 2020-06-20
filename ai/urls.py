from django.urls import path
from . import views


app_name = 'ai'
urlpatterns = [
    path('', views.ai_panel, name='ai_panel'),
    path('base/', views.base, name='base'),
    path('breast_cancer_detection/', views.breast_cancer_detection, name='breast_cancer_detection'),
    path('female_diabetes_detection/', views.female_diabetes_detection, name='female_diabetes_detection'),
    path('DNA_Classification/', views.DNA_Classification, name='DNA_Classification'),
    path('heart_disease_prediction/', views.heart_disease_prediction, name='heart_disease_prediction'),
    path('pneumonia_detection/', views.pneumonia_detection, name='pneumonia_detection'),
    path('recommend_to_me/', views.recommend_to_me, name='recommend_to_me'),
]
