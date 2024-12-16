from django.contrib import admin
from .models import Service, Master, Appointment

admin.site.register(Service)
admin.site.register(Master)
admin.site.register(Appointment)