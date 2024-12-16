from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    equipment = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class Master(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    experience = models.IntegerField()
    car_brands = models.TextField()
    photo = models.ImageField(upload_to='masters/')
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    car_brand = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    issue = models.TextField()
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    
    def __str__(self):
        return f"{self.name} - {self.preferred_date}"