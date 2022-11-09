from email.policy import default
from django.db import models
from django.urls import reverse
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from django.utils import timezone
#from django.core.validators import MaxValueValidator, MinValueValidator
#from phone_number_field.modelfields import PhoneNumberField
# Create your models here.
#-------------------------------------------------------------------------------
                    #USERS MODEL!!
#----------------------------------------------------------------------------
class User(AbstractUser):
    STAFF = 'staff'
    APPLICANT = 'applicant'

    user_types = [
        (STAFF, 'staff'),
        (STAFF, 'applicant')
    ]
    
    contact = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=user_types)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        """Return the url to access a particular user"""
        return reverse('user-details', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
      super().save(*args, **kwargs)


class Applicant(models.Model):   
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True, related_name='applicant')
    #To be able to view the name of the applicant in the table
    def __str__(self):
        return self.user
    
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True, related_name='staff')
    def __str__(self):
        return self.user
#---------------------------------------------------------------------------
                    #APPLICANT MODEL!!
#--------------------------------------------------------------------------------------------------------------
#staff model(jobs)
CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
)

class Job(models.Model):
    staff = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    skills_req = models.CharField(max_length=200, null=True, editable=True)
    job_type = models.CharField(max_length=30, choices=CHOICES, default='Full Time', null=True)
    link = models.URLField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    grad_year = models.IntegerField(blank=True)
    job_type = models.CharField(max_length=30, choices=CHOICES, default='Full Time', null=True)
    slug = AutoSlugField(populate_from='user', unique=True)

    def get_absolute_url(self):
        return "/profile/{}".format(self.slug)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    skill = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, related_name='skills', on_delete=models.CASCADE)


class SavedJobs(models.Model):
    job = models.ForeignKey(Job, related_name='saved_job', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='saved', on_delete=models.CASCADE)
    date_posted = models.DateTimeField (default=timezone.now )

    def __str__(self):
        return self.job.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=CASCADE)
    date_applied = models.DateTimeField()
    cover_letter = models.FileField(upload_to='applications/', null=True, blank=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=SET_NULL)
    date_approved = models.DateTimeField()


class AppliedJobs(models.Model):
    job = models.ForeignKey(Job, related_name='applied_job', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applied_user', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return self.job.title

#-------------------------------------------------------------------------------------------------
                      #STAFF MODEL!!
#-------------------------------------------------------------------------------------------------------
class Candidates(models.Model):
    job = models.ForeignKey(Job, related_name='candidates', on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, related_name='applied', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.candidate

class Selected(models.Model):
    job = models.ForeignKey(Job, related_name='select_job', on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, related_name='select_candidate', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.candidate
#-----------------------------------------------------------------------------------------------