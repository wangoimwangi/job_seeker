from django.db import models
from django.urls import reverse
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from django.utils import timezone
from django.db.models import UniqueConstraint

JOB_TYPES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
)

APPLICATION_STATUS = (
    ('pending', 'Pending'),
    ('in_process', 'In Process'),
    ('shortlisted', 'Shortlisted'),
    ('rejected', 'Rejected'),
)


class User(AbstractUser):
    STAFF = 'staff'
    APPLICANT = 'applicant'

    user_types = [
        (STAFF, 'staff'),
        (APPLICANT, 'applicant'),
    ]

    contact = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=20, choices=user_types, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('user-details', args=[str(self.id)])

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username

    @property
    def initials(self):
        parts = self.full_name.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return self.username[:2].upper()

    def __str__(self):
        return f'{self.full_name}: {self.user_type}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True, related_name='applicant')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    grad_year = models.IntegerField(blank=True, null=True)
    job_type = models.CharField(max_length=30, choices=JOB_TYPES, default='Full Time')

    def __str__(self):
        return self.user.full_name


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True, related_name='staff')

    class Meta:
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'

    def __str__(self):
        return self.user.full_name


class Job(models.Model):
    staff = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    skills_req = models.CharField(max_length=500, null=True, blank=True)
    job_type = models.CharField(max_length=30, choices=JOB_TYPES, default='Full Time', null=True)
    link = models.URLField(null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_skills_list(self):
        if self.skills_req:
            return [s.strip() for s in self.skills_req.split(',') if s.strip()]
        return []

    def applicant_count(self):
        return self.application_set.count()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    grad_year = models.IntegerField(blank=True, null=True)
    job_type = models.CharField(max_length=30, choices=JOB_TYPES, default='Full Time', null=True)
    slug = AutoSlugField(populate_from='user', unique=True)
    linkedin_url = models.URLField(blank=True, null=True, verbose_name='LinkedIn Profile URL')

    class Meta:
        verbose_name = 'Applicant Profile'
        verbose_name_plural = 'Applicant Profiles'

    def get_absolute_url(self):
        return '/profile/{}'.format(self.slug)

    def __str__(self):
        return self.user.username

    def completion_percentage(self):
        fields = [self.full_name, self.location, self.resume, self.grad_year, self.job_type]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)


class Skill(models.Model):
    skill = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='skills', on_delete=models.CASCADE)

    def __str__(self):
        return self.skill


class SavedJobs(models.Model):
    job = models.ForeignKey(Job, related_name='saved_job', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='saved', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)  # kept original name

    class Meta:
        unique_together = ['job', 'user']
        verbose_name = 'Saved Job'
        verbose_name_plural = 'Saved Jobs'

    def __str__(self):
        return self.job.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=CASCADE, related_name='applications')
    date_applied = models.DateTimeField(default=timezone.now)
    resume = models.FileField(upload_to='applications/resumes/', null=True, blank=True, verbose_name='Resume/CV')
    cover_letter = models.FileField(upload_to='cover_letters/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending')
    reviewed_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=SET_NULL, related_name='reviewed_applications')
    date_reviewed = models.DateTimeField(blank=True, null=True)

    # Keep legacy fields for compatibility
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=SET_NULL)
    date_approved = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['job', 'applicant'], name='unique_applicant_job_match')
        ]
        ordering = ['-date_applied']

    def __str__(self):
        return f'{self.applicant} applied for {self.job}'

    def get_status_color(self):
        colors = {
            'pending': 'warning',
            'in_process': 'info',
            'shortlisted': 'success',
            'rejected': 'danger',
        }
        return colors.get(self.status, 'secondary')


# Legacy models kept for backward compatibility
class AppliedJobs(models.Model):
    job = models.ForeignKey(Job, related_name='applied_job', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applied_user', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Applied Job'
        verbose_name_plural = 'Applied Jobs'

    def __str__(self):
        return self.job.title


class Candidates(models.Model):
    job = models.ForeignKey(Job, related_name='candidates', on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, related_name='applied', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'


class Selected(models.Model):
    job = models.ForeignKey(Job, related_name='select_job', on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, related_name='select_candidate', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Selection'
        verbose_name_plural = 'Selections'
