from django.db import models
from django.urls import reverse
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import AbstractUser

from django.core.validators import MaxValueValidator, MinValueValidator
#from phone_number_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    STAFF = 'staff'
    APPLICANT = 'applicant'
    
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    user_type = [
        (APPLICANT, 'applicant'),
        (STAFF, 'staff')
    ]

    def get_absolute_url(self):
        return reverse("user-details", args={"id": self.id})

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
      super().save(*args, **kwargs)



class Applicant(models.Model):   
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True, related_name='applicant')
    qualifications = models.TextField()

    #To be able to view the name of the applicant in the table
    def __str__(self):
        return self.name
    

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True, related_name='staff')
    company = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class JobCategory(models.Model):
    category_name = models.CharField(max_length=100)


class Job(models.Model):
    category = models. ForeignKey(JobCategory, on_delete=SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100)
    hours = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    salary = models.IntegerField()
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=100)
    qualification = models.TextField(max_length=500)
    status = models.CharField(max_length=100)


class JobApplication(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=CASCADE, related_name='applicant')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job')

    