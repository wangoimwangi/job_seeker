from django import forms
#from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from job_seeker.models import Staff, User
from job_seeker.models import Profile, Skill
from job_seeker.models import Job
from job_seeker.models import Applicant
#----------------------------------------------------------------------------------------------------
                         #REGISTRATION FORM!(USER)
#---------------------------------------------------------------------------------------------------
class StaffRegistrationForm(UserCreationForm):
    """Staff registration form"""
    first_name = forms.CharField(required=True)  
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    contact = forms.CharField(required=True)
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
      model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False) # saves username, password [UserCreationForm fields]
        user.contact = self.cleaned_data['contact']
        user.location = self.cleaned_data['location']
        user.email = self.cleaned_data['email']
        user.user_type = User.STAFF
        user.save()

        staff = Staff.objects.create(user=user)
        staff.save()
        return user


class ApplicantRegistrationForm(UserCreationForm):
    """Applicant registration form"""
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    contact = forms.CharField(required=True)
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
      model = User

    @transaction.atomic
    def save(self):
        # saves username, password [UserCreationForm fields]
        user = super().save(commit=False)
        user.contact = self.cleaned_data['contact']
        user.location = self.cleaned_data['location']
        user.email = self.cleaned_data['email']
        user.user_type = User.APPLICANT
        user.save()

        applicant = Applicant.objects.create(user=user)
        applicant.save()
        return user
#----------------------------------------------------------------------------------------------------------
                             #APPLICANT FORMS!
#----------------------------------------------------------------------------------------------------------------
                    #PROFILE UPDATE FORM
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name','location',
                  'resume', 'grad_year', 'job_type']
#------------------------------------------------------------------------------------------------------------
                    #NEWSKILLS FORM
class NewSkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill']
#---------------------------------------------------------------------------------------------------------
                #STAFF FORMS!
#-----------------------------------------------------------------------------------------
                 #NEWJOBFORM
class NewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location','description', 'skills_req', 'job_type', 'link']
        help_texts = {'skills_req': 'Enter all the skills required each separated by commas.','link': 'If you want candidates to apply on your company website rather than on our website, please provide the link where candidates can apply. Otherwise, please leave it blank or candidates would not be able to apply directly!',
        }
#-----------------------------------------------------------------------------------------------
                     #JOBUPDATEFORM
class JobUpdateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location',
                  'description', 'skills_req', 'job_type', 'link']
        help_texts = {'skills_req': 'Enter all the skills required each separated by commas.',
                      'link': 'If you want candidates to apply on your company website rather than on our website, please provide the link where candidates can apply. Otherwise, please leave it blank or candidates would not be able to apply directly!',
        }
#------------------------------------------------------------------------------------------------------------