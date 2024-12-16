from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('masters/', views.masters, name='masters'),
    path('diagnostics/', views.diagnostics, name='diagnostics'),
    path('appointment/', views.appointment, name='appointment'),
]