from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from django.core.mail import send_mail

# @receiver(post_save, sender=Appointment)
# def send_appointment_notification(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#             'Новая запись в автосервис',
#             f'Клиент {instance.name} записался на {instance.preferred_date} {instance.preferred_time}. \n'
#             f'Марка авто: {instance.car_brand}\n'
#             f'Услуга: {instance.service}\n'
#             f'Проблема: {instance.issue}',
#             'from@example.com',
#             ['your-email@example.com'],
#             fail_silently=False,
#         )