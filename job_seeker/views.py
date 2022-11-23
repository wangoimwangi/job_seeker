#GENERAL IMPORTS
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .filters import ApplicationFilter
#--------------------------------------------------------------
#APPLICANT IMPORTS
import datetime as DT
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
#---------------------------------------------------------------------------
#STAFF IMPORTS
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.contrib.auth.models import User
#-----------------------------------------------------------------------------------------
from .models import *
from .forms import *
from .decorators import *
# from .filters import *
#-------------------------------------------------------------------------------
                              #USERS VIEWS
#-------------------------------------------------------------------------------
#HOME
def home(request):
    context = {
        'home': "active",
    }
    return render(request, 'jobseeker/home.html', context)
#APPLICANT
def applicant(request):
    context = {
        'applicant': "active",
    }
    return render(request, 'applicant/applicant.html', context)
#STAFF
def staff(request):
    context = {
        'staff': "active",
    }
    return render(request, 'staff/staff.html',context)
#CONTACT
def contact(request):
    context = {
        'contact': "active",
    }
    return render(request, 'jobseeker/contact.html', context)
#SERVICES
def Services(request):
    context = {
        'services': "active",
    }
    return render(request, 'jobseeker/services.html', context)

#------------------------------------------------------------------------------------------
                  #LOGIN!
def user_login(request):
    if not request.method == 'POST':
        login_form = AuthenticationForm()
        return render(request, 'jobseeker/login.html', context={'form': login_form})
    form = AuthenticationForm(data=request.POST)
    if not form.is_valid():
      messages.error(request, form.errors) 
      return redirect('login')
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)

    user = User.objects.get(pk=user.id)

    if user.user_type == User.APPLICANT:
      login(request, user)
      messages.success(request, 'Successfully logged in!')
      return redirect('applicant')
    
    elif user.user_type == User.STAFF:
        login(request, user)
    messages.success(request, 'Successfully logged in!')
    return redirect('staff')

#-------------------------------------------------------------------------------------------------
                          #LOGOUT!
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')
#======================================================================================================
                    #REGISTRATION PART
def register(request):
    return render(request, 'jobseeker/register.html')

class RegisterStaff(CreateView):
    form_class = StaffRegistrationForm
    template_name = 'staff/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return redirect('staff')


class RegisterApplicant(CreateView):
    form_class = ApplicantRegistrationForm
    template_name = 'applicant/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return redirect('applicant')

def staff(request):
     return render(request, 'staff/staff.html')


def applicant(request):
    return render(request, 'applicant/applicant.html')
#-------------------------------------------------------------------------------------
                        #APPLICANT VIEWS
#===========================================================================================
                        #PROFILE!
#Displays the user profile and skills and add newskills 
@login_required
def my_profile(request):
    you = request.user
    profile = Profile.objects.filter(user=you).first()
    user_skills = Skill.objects.filter(user=you)
    if request.method == 'POST':
        form = NewSkillForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = you
            data.save()
            return redirect('my-profile')
    else:
        form = NewSkillForm()
    context = {
        'u': you,
        'profile': profile,
        'skills': user_skills,
        'form': form,
        'profile_page': "active",
    }
    return render(request, 'applicant/profile.html', context)
#----------------------------------------------------------------------------------------------------
                   #EDIT_PROFILE
#Appliants are able to edit their profiles
@login_required
def edit_profile(request):
    you = request.user
    profile = Profile.objects.filter(user=you).first()
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = you
            data.save()
            return redirect('my-profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    context = {
        'form': form,
    }
    return render(request, 'applicant/edit_profile.html', context)
#-------------------------------------------------------------------------------------------------------
                                  #PROFILE VIEW
@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    you = p.user
    user_skills = Skill.objects.filter(user=you)
    context = {
        'u': you,
        'profile': p,
        'skills': user_skills,
    }
    return render(request, 'applicant/profile.html', context)
#------------------------------------------------------------------------------------------------
                    #POSTED JOBS
def posted_jobs(request):
    jobs = Job.objects.all()
    already_applied = []    # list of IDs of the job current applicant has applied to

    if request.user.user_type == User.APPLICANT:
        for application in request.user.applicant.application_set.all():
            already_applied.append(application.job.id)

    context = {
        'jobs': jobs
    }
    if request.user.user_type == User.APPLICANT:
        context['already_applied'] = already_applied

    if request.user.user_type == User.STAFF:
        context['applicants'] = list()

    return render(request, 'jobseeker/posted_jobs.html', context)
#----------------------------------------------------------------------------------------------
                   #JOB _DETAILS
def job_details(request, job_id):
    user = request.user
    job = Job.objects.get(id=job_id)
    already_applied = False
    # compare the skills in the job with those all the user
    relevant_jobs = list()

    if user.user_type == User.APPLICANT:
        for application in user.applicant.application_set.all():
            if application.job.id == job.id:
                already_applied = True

    context = {}
    context['job'] = job
    context['relevant_jobs'] = relevant_jobs

    if user.user_type == User.APPLICANT:
        context['already_applied'] = already_applied

    if user.user_type == User.STAFF:
        context['applications'] = Application.objects.filter(job_id=job_id)      

    return render(request, 'jobseeker/job_detail.html', context)


@staff_required
def application_details(request, application_id):
    application = Application.objects.get(id=application_id)

    if request.method == 'POST':
        action = request.POST['action']

        if action == 'decline':
            application.approved = False
            application.approved_by = request.user.staff
            application.date_approved = DT.datetime.now()
            application.save()
            # notify user
            
        if action == 'approve':
            # update the db
            application.approved = True
            application.approved_by = request.user.staff
            application.date_approved = DT.datetime.now()
            application.save()
            # notify user
            
        return redirect('job-details', application.job.id)

    else:
        context = {}
        context['application'] = application
        return render(request, 'staff/application-details.html', context)

#----------------------------------------------------------------------------------------------------------------
                        #DELETE SKILL
#A CSRF cookie used is a random secret value, which other sites will not have access to
@login_required
@csrf_exempt
def delete_skill(request, pk=None):
    if request.method == 'POST':
        id_list = request.POST.getlist('choices')
        for skill_id in id_list:
            Skill.objects.get(id=skill_id).delete()
        return redirect('my-profile')
#-------------------------------------------------------------------------------------------
                  #SAVED JOBS
#Display all the jobs that the user has saved
@login_required
def saved_jobs(request):
    jobs = SavedJobs.objects.filter(
    user=request.user).order_by('-date_posted')
    return render(request, 'applicant/saved_jobs.html', {'jobs': jobs,})
#-------------------------------------------------------------------------------------
                     #SAVE JOB
#Applicant is able to save a job of their choice and store it for future viewing
#The saved job is added to the saved job model
@login_required
def save_job(request, slug):
       user = request.user
       job = get_object_or_404(Job, slug=slug)
       saved, created = SavedJobs.objects.get_or_create(job=job, user=user)
       return HttpResponseRedirect('/job/{}'.format(job.slug))
#---------------------------------------------------------------------------
                          #APPLY JOB
#Applicant is able to apply to a job
@login_required
def apply_job(request, job_id):
    if not request.method == 'POST':
        form = JobApplicationForm()
        job = Job.objects.get(id=job_id)
        context = {
            'form': form,
            'job': job
        }
        return render(request, 'applicant/apply.html', context)

    form = JobApplicationForm(request.POST)
    if not form.is_valid():
        # msg
        return redirect(request.META.get('HTTP_REFERER'))
    # get cover letter from the form
    cover_letter = form.cleaned_data['cover_letter']
    # generate current date from datetime
    time_submitted = DT.datetime.now()
    # create an Application
    application = Application.objects.create(
        job_id=job_id,
        applicant_id=request.user.id,
        date_applied=time_submitted,
        cover_letter=cover_letter
    )
    application.save()
    return redirect('posted-jobs')
#------------------------------------------------------------------------------
                  #APPLIED JOBS
#Show the status of the application(selected,rejected or pending)
@login_required
def applied_jobs(request):
    jobs = AppliedJobs.objects.filter(
        user=request.user).order_by('-date_posted')
    statuses = []
    for job in jobs:
        if Selected.objects.filter(job=job.job).filter(candidate=request.user).exists():
            statuses.append(0)
        elif Candidates.objects.filter(job=job.job).filter(candidate=request.user).exists():
            statuses.append(1)
        else:
            statuses.append(2)
    zipped = zip(jobs, statuses)
    return render(request, 'applicant/applied_jobs.html', {'zipped': zipped})
#---------------------------------------------------------------------------------------------------------
                        #STAFF VIEWS!!
#=================================================================================================
                    #ADD JOBS
#Used by the staff to add a new job post
#Redirect to the job list page
@login_required
def add_job(request):
    user = request.user
    if request.method == 'POST':
        form = NewJobForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.staff = user
            data.save()
            return redirect('job-list')
    else:
        form = NewJobForm()
        context = {
            'add_job_page': "active",
            'form': form,
        }
        return render(request, 'staff/add_job.html', context)
#-----------------------------------------------------------------------------
                  #EDIT JOB
#Used to update job post
#Redirects to job details page
@login_required
def edit_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    if request.method == "POST":
        form = NewJobForm(request.POST, instance=job)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('job-details',job.id)
    else:
        form = NewJobForm(instance=job)
    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'staff/edit_jobs.html', context)
#----------------------------------------------------------------------------------------
                    #ALL JOBS
#Display all jobs posted by the staff
#Has a paginator to restrict the job posts to 10 per page
@login_required
def all_jobs(request):
    jobs = Job.objects.filter(staff=request.user).order_by('-date_posted')
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'manage_jobs_page': "active",
        'jobs': page_obj,
    }
    return render(request, 'staff/job_post.html', context)
#---------------------------------------------------------------------------------------------
                        #APPLICANTS SEARCH
#Allows staff to search for an applicant based on location and job type
#Have access to the applicants resumes 
@login_required
def search_applicant(request):
    profile_list = Profile.objects.all()
    profiles = []
    for profile in profile_list:
        if profile.resume and profile.user != request.user:
            profiles.append(profile)

    rec1 = request.GET.get('r')
    rec2 = request.GET.get('s')

    if rec1 == None:
        li1 = Profile.objects.all()
    else:
        li1 = Profile.objects.filter(location__icontains=rec1)

    if rec2 == None:
        li2 = Profile.objects.all()
    else:
        li2 = Profile.objects.filter(job_type__icontains=rec2)

    final = []
    profiles_final = []

    for i in li1:
        if i in li2:
            final.append(i)

    for i in final:
        if i in profiles:
            profiles_final.append(i)

    paginator = Paginator(profiles_final, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'search_applicant_page': "active",
        'profiles': page_obj,
    }
    return render(request, 'staff/applicant_search.html', context)
#-----------------------------------------------------------------------------------
#RELEVANT APPLICANT
@login_required
def job_candidate_search(request, slug):
    job = get_object_or_404(Job, slug=slug)
    relevant_candidates = []
    common = []
    applicants = Profile.objects.filter(job_type=job.job_type)
    job_skills = []
    skills = str(job.skills_req).split(",")
    for skill in skills:
        job_skills.append(skill.strip().lower())
    for applicant in applicants:
        user = applicant.user
        skill_list = list(Skill.objects.filter(user=user))
        skills = []
        for i in skill_list:
            skills.append(i.skill.lower())
        common_skills = list(set(job_skills) & set(skills))
        if (len(common_skills) != 0 and len(common_skills) >= len(job_skills)//2):
            relevant_candidates.append(applicant)
            common.append(len(common_skills))
    objects = zip(relevant_candidates, common)
    objects = sorted(objects, key=lambda t: t[1], reverse=True)
    objects = objects[:100]
    context = {
        'job': job,
        'objects': objects,
        'job_skills': len(job_skills),
        'relevant': len(relevant_candidates),

    }
    return render(request, 'staff/job_applicant_search.html', context)



                      

                                 
