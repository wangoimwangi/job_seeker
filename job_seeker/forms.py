from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Staff, User, Profile, Skill, Job, Applicant, Application


class StaffRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Work email address'})
    )
    contact = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '+254 700 000 000'})
    )
    location = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'City, Country'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'contact', 'location', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.user_type = User.STAFF
        user.contact = self.cleaned_data['contact']
        user.location = self.cleaned_data['location']
        user.save()
        Staff.objects.create(user=user)
        return user


class ApplicantRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Your email address'})
    )
    contact = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '+254 700 000 000'})
    )
    location = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'City, Country'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'contact', 'location', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.user_type = User.APPLICANT
        user.contact = self.cleaned_data['contact']
        user.location = self.cleaned_data['location']
        user.save()
        Applicant.objects.create(user=user)
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'location', 'resume', 'grad_year', 'job_type', 'linkedin_url']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
            'grad_year': forms.NumberInput(attrs={'placeholder': 'e.g. 2024', 'min': 1990, 'max': 2030}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourname'}),
        }


class NewSkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill']
        widgets = {
            'skill': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, React'})
        }


class NewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'description', 'skills_req', 'job_type', 'salary', 'deadline', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Senior Software Engineer'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company name'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Nairobi, Kenya'}),
            'description': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Describe the role, responsibilities, and what you are looking for...'
            }),
            'skills_req': forms.TextInput(attrs={
                'placeholder': 'e.g. Python, Django, PostgreSQL, REST APIs'
            }),
            'salary': forms.TextInput(attrs={'placeholder': 'e.g. KES 80,000 - 120,000/month'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://company.com/careers/job'}),
        }
        help_texts = {
            'skills_req': 'Enter skills separated by commas.',
            'link': 'Optional: external application link. Leave blank to accept applications here.',
        }


class JobApplicationForm(forms.ModelForm):
    resume = forms.FileField(
        required=False,
        label='Resume/CV',
        help_text='Upload a CV tailored for this specific role. PDF, DOC or DOCX. Max 5MB.',
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
    )

    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'})
        }
