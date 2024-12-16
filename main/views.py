from django.shortcuts import render, redirect
from .models import Service, Master, Appointment
from .forms import AppointmentForm
from django.contrib import messages

def index(request):
    services = Service.objects.all()[:3]
    masters = Master.objects.all()[:3]
    return render(request, 'main/index.html', {'services': services, 'masters': masters})

def services(request):
    services = Service.objects.all()
    return render(request, 'main/services.html', {'services': services})

def masters(request):
    masters = Master.objects.all()
    return render(request, 'main/masters.html', {'masters': masters})

def diagnostics(request):
    return render(request, 'main/diagnostics.html')

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка успешно отправлена!')
            return redirect('appointment')
    else:
        form = AppointmentForm()
    return render(request, 'main/appointment.html', {'form': form})