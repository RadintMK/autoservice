import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Service, Master, Appointment
from .forms import AppointmentForm
from rest_framework.test import APIClient

# Модель Master теперь включает experience
class MasterModelTest(TestCase):
    def test_master_creation(self):
        """Проверка создания мастера."""
        master = Master.objects.create(
            name="Иванов",
            specialization="Двигатели",
            experience=5  # Добавлено обязательное поле
        )
        self.assertEqual(master.name, "Иванов")
        self.assertEqual(master.specialization, "Двигатели")
    
    def test_master_str(self):
        """Проверка строкового представления мастера."""
        master = Master.objects.create(
            name="Петров",
            specialization="Ходовая",
            experience=3
        )
        self.assertEqual(str(master), "Петров (Ходовая)")  # Исправлен формат

class ServiceModelTest(TestCase):
    def test_service_str(self):
        """Проверка строкового представления услуги."""
        service = Service.objects.create(
            name="Замена масла",
            description="Смена моторного масла",
            price=1500
        )
        self.assertEqual(str(service), "Замена масла (1500 руб.)")  # Добавлен формат
    
    def test_service_price_validation(self):
        """Проверка валидации отрицательной цены."""
        service = Service(name="Тест", price=-100)
        with self.assertRaises(ValueError):  # Добавлено ожидание исключения
            service.save()

class AppointmentModelTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Ремонт тормозов",
            price=2500
        )
        self.master = Master.objects.create(  # Добавлено experience
            name="Сидоров",
            specialization="Тормозная система",
            experience=7
        )
    
    def test_appointment_str(self):
        """Проверка строкового представления записи."""
        appointment = Appointment.objects.create(
            name="Клиент1",
            phone="+79001234567",
            service=self.service,
            preferred_date=timezone.localdate(),
            preferred_time="10:00",
            master=self.master  # Добавлено обязательное поле
        )
        self.assertEqual(
            str(appointment),
            "Запись: Клиент1 на " + str(timezone.localdate()) + " 10:00 (Мастер: Сидоров)"
        )
    
    def test_appointment_unique_time(self):
        """Проверка уникальности времени записи."""
        Appointment.objects.create(
            service=self.service,
            preferred_date=timezone.localdate(),
            preferred_time="15:00",
            master=self.master
        )
        with self.assertRaises(Exception):
            Appointment.objects.create(
                service=self.service,
                preferred_date=timezone.localdate(),
                preferred_time="15:00",
                master=self.master
            )

class AppointmentFormTest(TestCase):
    def test_valid_form(self):
        """Проверка валидной формы."""
        data = {
            "name": "Клиент2",
            "phone": "+79001234567",
            "service": self.service.id,
            "preferred_date": "2023-10-05",
            "preferred_time": "14:00",
            "master": self.master.id  # Добавлено обязательное поле
        }
        form = AppointmentForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_phone(self):
        """Проверка невалидного номера телефона."""
        data = {
            "phone": "1234567"  # Неверный формат
        }
        form = AppointmentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.service = Service.objects.create(
            name="Диагностика",
            price=1000
        )
        self.master = Master.objects.create(
            name="Мастер1",
            specialization="Электрика",
            experience=2
        )
    
    def test_home_view(self):
        """Проверка доступности главной страницы."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
    
    def test_appointment_create_view(self):
        """Проверка создания записи через форму."""
        data = {
            "name": "Иванов",
            "phone": "+79001234567",
            "service": self.service.id,
            "preferred_date": "2023-10-06",
            "preferred_time": "09:00",
            "master": self.master.id  # Добавлено обязательное поле
        }
        response = self.client.post(reverse("create_appointment"), data)
        self.assertEqual(response.status_code, 302)  # Редирект после успеха
        self.assertEqual(Appointment.objects.count(), 1)
    
    def test_duplicate_appointment(self):
        """Проверка блокировки дублирующей записи."""
        Appointment.objects.create(
            service=self.service,
            preferred_date="2023-10-07",
            preferred_time="12:00",
            master=self.master
        )
        data = {
            "service": self.service.id,
            "preferred_date": "2023-10-07",
            "preferred_time": "12:00",
            "master": self.master.id
        }
        response = self.client.post(reverse("create_appointment"), data)
        self.assertFormError(
            response,
            "form",
            "preferred_time",
            "Это время уже занято"
        )

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.service = Service.objects.create(
            name="Ремонт двигателя",
            price=3000
        )
        self.master = Master.objects.create(
            name="Мастер2",
            specialization="Двигатели",
            experience=4
        )
    
    def test_service_list_api(self):
        """Проверка получения списка услуг через API."""
        response = self.client.get(reverse("api:service-list"))  # Используем URL-имя
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Service.objects.count())
    
    def test_appointment_creation_api(self):
        """Проверка создания записи через API."""
        data = {
            "name": "Клиент3",
            "phone": "+79001234567",
            "service": self.service.id,
            "preferred_date": "2023-10-08",
            "preferred_time": "11:00",
            "master": self.master.id
        }
        response = self.client.post(reverse("api:appointment-create"), data)  # Используем URL-имя
        self.assertEqual(response.status_code, 201)  # Success creation

class SecurityTest(TestCase):
    def test_csrf_protection(self):
        """Проверка CSRF-токена в форме."""
        response = self.client.get(reverse("create_appointment"))
        self.assertContains(response, "csrfmiddlewaretoken")
    
    def test_xss_protection(self):
        """Проверка защиты от XSS в шаблонах."""
        data = {
            "name": "<script>alert('XSS')</script>",
            "phone": "+79001234567",
            "service": 1,
            "preferred_date": "2023-10-09",
            "preferred_time": "10:00",
            "master": self.master.id
        }
        response = self.client.post(reverse("create_appointment"), data)
        self.assertEqual(response.status_code, 200)  # Форма не должна пройти валидацию
        self.assertFormError(
            response,
            "form",
            "name",
            "Недопустимые символы в имени"
        )

# Дополнительные тесты для покрытия всех полей
class AppointmentValidationTest(TestCase):
    def test_future_date(self):
        """Проверка валидации даты в будущем."""
        appointment = Appointment(
            preferred_date=timezone.localdate()
        )
        self.assertTrue(appointment.is_valid_date())
    
    def test_past_date(self):
        """Проверка блокировки прошедшей даты."""
        appointment = Appointment(
            preferred_date=timezone.localdate() - timezone.timedelta(days=1)
        )
        self.assertFalse(appointment.is_valid_date())