#from ast import Return
#from multiprocessing import context
#from jobs. jobs.job_seeker.models import Applicant
# from django.contrib.auth.forms import UserCreationForm
# from django.forms import inlineformset_factory
#------------------------------------------------------------------------
#USER IMPORTS
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#--------------------------------------------------------------
#APPLICANT IMPORTS
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from job_seeker.models import Job, Candidates, Selected
from job_seeker.models import Profile, Skill, AppliedJobs, SavedJobs
from job_seeker.forms import ProfileUpdateForm, NewSkillForm
#---------------------------------------------------------------------------
#STAFF IMPORTS
from job_seeker.forms import NewJobForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.contrib.auth.models import User
#----------------------------------------------------------------------
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
#-----------------------------------------------------------------------------------------
from .models import *
from .forms import *
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
    return render(request, 'staff/staff.html') #,context)



#------------------------------------------------------------------------------------------
                  #LOGIN AND LOGOUT!
def user_logout(request):
    return render(request, 'jobseeker/logout.html')

def user_login(request):
    if not request.method == 'POST':
        login_form = AuthenticationForm()
        print(User.STAFF)
        return render(request, 'jobseeker/login.html', context={'form': login_form})
    form = AuthenticationForm(data=request.POST)
    if not form.is_valid():
      messages.error(request, form.errors) 
      return redirect('login')
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)
    if user is None:
      messages.error(request, 'Invalid username or password!')
      return redirect('login')
    login(request, user)
    messages.success(request, 'Successfully logged in!')
    #return redirect('home')
    return redirect('applicant')

#user = User.objects.get(pk=user.id)
#print(f'\n\nUser Type: {user.user_type}\n\n')
#if user.user_type == User.STAFF:
    #print('\n\n User is staff! \n\n')
    #return redirect('staff_jobs')
#elif user.user_type == User.APPLICANT:
            #pass
    #return redirect('my-profile')#'home'


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')
#----------------------------------------------------------------------------------------------------
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
        return redirect('add-job')


class RegisterApplicant(CreateView):
    form_class = ApplicantRegistrationForm
    template_name = 'applicant/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        #print('\n\nLogin successful!\n\n')
        # messages.success(self.request, 'Registration successful!')
        return redirect('applied-jobs')

#def staff_jobs(request):
    #return render(request, 'staff/jobs.html')


#def applied_jobs(request):
    #return render(request, 'applied_jobs.html')
#-------------------------------------------------------------------------------------
                        #APPLICANT VIEWS
#------------------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------
               #PROFILE_VIEW(FOR STAFF)
#For staff to view the Applicants Profiles
#No edit of skills
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
#def candidate_details(request):
    #return render(request, 'candidates/details.html')
#-----------------------------------------------------------------------------------------------
                        #JOB_SEARCH_LIST
# Make a list which consists of jobs which applicant will seewhen he clicks the search button
#No input display all jobs

def job_search_list(request):
    query = request.GET.get('p')
    loc = request.GET.get('q')
    object_list = []
    if (query == None):
        object_list = Job.objects.all()
    else:
        title_list = Job.objects.filter(
            title__icontains=query).order_by('-date_posted')
        skill_list = Job.objects.filter(
            skills_req__icontains=query).order_by('-date_posted')
        company_list = Job.objects.filter(
            company__icontains=query).order_by('-date_posted')
        job_type_list = Job.objects.filter(
            job_type__icontains=query).order_by('-date_posted')
        for i in title_list:
            object_list.append(i)
        for i in skill_list:
            if i not in object_list:
                object_list.append(i)
        for i in company_list:
            if i not in object_list:
                object_list.append(i)
        for i in job_type_list:
            if i not in object_list:
                object_list.append(i)
    if (loc == None):
        locat = Job.objects.all()
    else:
        locat = Job.objects.filter(
            location__icontains=loc).order_by('-date_posted')
    final_list = []
    for i in object_list:
        if i in locat:
            final_list.append(i)
            #apply a paginator to restrict each page of the search result in 20 job posts.
    paginator = Paginator(final_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'jobs': page_obj,
        'query': query,
    }
    return render(request, 'applicant/job_search_list.html', context)
#-------------------------------------------------------------------------------------------------------
                         #JOB_DETAIL
#It will display the job post in details and has a apply and save button.
#Make a list which consist of the job similiar to the ones selected
#slug is a way of generating a valid URL, generally using data already obtained.

def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    apply_button = 0
    save_button = 0
    profile = Profile.objects.filter(user=request.user).first()
    if AppliedJobs.objects.filter(user=request.user).filter(job=job).exists():
        apply_button = 1
    if SavedJobs.objects.filter(user=request.user).filter(job=job).exists():
        save_button = 1
    relevant_jobs = []
    jobs1 = Job.objects.filter(
        company__icontains=job.company).order_by('-date_posted')
    jobs2 = Job.objects.filter(
        job_type__icontains=job.job_type).order_by('-date_posted')
    jobs3 = Job.objects.filter(
        title__icontains=job.title).order_by('-date_posted')
    for i in jobs1:
        if len(relevant_jobs) > 5:
            break
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)
    for i in jobs2:
        if len(relevant_jobs) > 5:
            break
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)
    for i in jobs3:
        if len(relevant_jobs) > 5:
            break
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)

    return render(request, 'applicant/job_detail.html', {'job': job, 'profile': profile, 'apply_button': apply_button, 'save_button': save_button, 'relevant_jobs': relevant_jobs, 'navbar': 1}) #'candidate_navbar': 1})

#---------------------------------------------------------------------------------------------------------------------------------
                       #SAVED JOBS
#Takes the saved jobs by the user and orders them in order of date posted.

@login_required
def saved_jobs(request):
    jobs = SavedJobs.objects.filter(
        user=request.user).order_by('-date_posted')
    return render(request, 'applicant/saved_jobs.html', {'jobs': jobs, 'navbar': 1})
#---------------------------------------------------------------------------------------------------
                      #APPLIED JOBS
#Display all the jobs the user has applied to
#Show the status of the application(selected,rejected or pending)

@login_required
def applied_jobs(request):
    jobs = AppliedJobs.objects.filter(
        user=request.user).order_by('-date_posted')
    statuses = []
    for job in jobs:
        if Selected.objects.filter(job=job.job).filter(applicant=request.user).exists():
            statuses.append(0)
        elif Candidates.objects.filter(job=job.job).filter(applicant=request.user).exists():
            statuses.append(1)
        else:
            statuses.append(2)
    zipped = zip(jobs, statuses)
    # 'candidate_navbar': 1})
    # 'candidate_navbar': 1})
    return render(request, 'applicant/applied_jobs.html', {'zipped': zipped})
#----------------------------------------------------------------------------------------------------------------------------
                     #INTELLIGENCE_SEARCH
#showapplicant jobs which suits the skill set of the user and matches the job type the user is looking for .
# The Higher the skill match percentage, higher the position it will occupy in the list.

@login_required
def intelligent_search(request):
    relevant_jobs = []
    common = []
    job_skills = []
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    my_skill_query = Skill.objects.filter(user=user)
    my_skills = []
    for i in my_skill_query:
        my_skills.append(i.skill.lower())
    if profile:
        jobs = Job.objects.filter(
            job_type=profile.looking_for).order_by('-date_posted')
    else:
        jobs = Job.objects.all()
    for job in jobs:
        skills = []
        sk = str(job.skills_req).split(",")
        for i in sk:
            skills.append(i.strip().lower())
        common_skills = list(set(my_skills) & set(skills))
        if (len(common_skills) != 0 and len(common_skills) >= len(skills)//2):
            relevant_jobs.append(job)
            common.append(len(common_skills))
            job_skills.append(len(skills))
    objects = zip(relevant_jobs, common, job_skills)
    objects = sorted(objects, key=lambda t: t[1]/t[2], reverse=True)
    objects = objects[:100]
    context = {
        'intel_page': "active",
        'jobs': objects,
        'counter': len(relevant_jobs),
    }
    return render(request, 'applicant/intelligent_search.html', context)
#----------------------------------------------------------------------------------------------------------------
                        #DELETE SKILL
#Applicant can select a skill and delete it 
#A CSRF cookie used is a random secret value, which other sites will not have access to

@login_required
@csrf_exempt
def delete_skill(request, pk=None):
    if request.method == 'POST':
        id_list = request.POST.getlist('choices')
        for skill_id in id_list:
            Skill.objects.get(id=skill_id).delete()
        return redirect('my_profile')
#-------------------------------------------------------------------------------------------
                            #SAVE JOB
#Applicant is able to save a job of their choice and store it for future viewing
#The saved job is added to the saved job model

@login_required
def save_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    saved, created = SavedJobs.objects.get_or_create(job=job, user=user)
    return HttpResponseRedirect('/job/{}'.format(job.slug))
#---------------------------------------------------------------------------------
                          #APPLY JOB
#Applicant is able to apply to a job
#Adds the job to Appliedjobs model and applicants model of the staff

@login_required
def apply_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    applied, created = AppliedJobs.objects.get_or_create(job=job, user=user)
    applicant, creation = Candidates.objects.get_or_create(
        job=job, applicant=user)
    return HttpResponseRedirect('/job/{}'.format(job.slug))
#------------------------------------------------------------------------------
                     #DELETE JOB
#Used to delete a job from the saved jobs list

@login_required
def remove_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    saved_job = SavedJobs.objects.filter(job=job, user=user).first()
    saved_job.delete()
    return HttpResponseRedirect('/job/{}'.format(job.slug))
#------------------------------------------------------------------------------
                        #STAFF VIEWS!!
#-----------------------------------------------------------------------------------------
                    #ADD JOBS
#Used by the staff to add a new job post
#Redirect to the job list page
@login_required
def add_job(request):
    user = request.user
    if request.method == "POST":
        form = NewJobForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.recruiter = user
            data.save()
            return redirect('job-list')
    else:
        form = NewJobForm()
    context = {
        'add_job_page': "active",
        'form': form,
        'rec_navbar': 1,
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
            return redirect('add-job-detail', slug)
    else:
        form = NewJobForm(instance=job)
    context = {
        'form': form,
        'rec_navbar': 1,
        'job': job,
    }
    return render(request, 'staff/edit_job.html', context)
#---------------------------------------------------------------------------
                    #JOB DETAILS
#Display the details of the job
@login_required
def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    context = {
        'job': job,
        'rec_navbar': 1,
    }
    return render(request, 'staff/job_detail.html', context)
#----------------------------------------------------------------------------------------
                    #ALL JOBS
#Display all jobs posted by the staff
#Has a paginator to restrict the job posts to 20 per page
@login_required
def all_jobs(request):
    jobs = Job.objects.filter(staff=request.user).order_by('-date_posted')
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'manage_jobs_page': "active",
        'jobs': page_obj,
        #'rec_navbar': 1,
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
        li2 = Profile.objects.filter(looking_for__icontains=rec2)

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
        'rec_navbar': 1,
        'profiles': page_obj,
    }
    return render(request, 'staff/applicant_search.html', context)
#--------------------------------------------------------------------------------
                       #JOB APPLICANT SEARCH
#Allows staff to see aplicants which are perfect matches to a particular job post
#It matches the skills set for a job with what the applicant set on their profile
#It filters out candidates based on job type
@login_required
def job_applicant_search(request, slug):
    job = get_object_or_404(Job, slug=slug)
    relevant_applicants = []
    common = []
    candidates = Profile.objects.filter(looking_for=job.job_type)
    job_skills = []
    skills = str(job.skills_req).split(",")
    for skill in skills:
        job_skills.append(skill.strip().lower())
    for candidate in candidates:
        user = candidate.user
        skill_list = list(Skill.objects.filter(user=user))
        skills = []
        for i in skill_list:
            skills.append(i.skill.lower())
        common_skills = list(set(job_skills) & set(skills))
        if (len(common_skills) != 0 and len(common_skills) >= len(job_skills)//2):
            relevant_applicants.append(candidate)
            common.append(len(common_skills))
    objects = zip(relevant_applicants, common)
    objects = sorted(objects, key=lambda t: t[1], reverse=True)
    objects = objects[:100]
    context = {
        'rec_navbar': 1,
        'job': job,
        'objects': objects,
        'job_skills': len(job_skills),
        'relevant': len(relevant_applicants),

    }
    return render(request, 'staff/job_applicant_search.html', context)
#-----------------------------------------------------------------------------------------
                      #CANDIDATES LIST
#Display candidates who have applied for a particular job


@login_required
def candidate_list(request, slug):
    job = get_object_or_404(Job, slug=slug)
    candidates = candidates.objects.filter(job=job).order_by('date_posted')
    profiles = []
    for candidate in candidates:
        profile = Profile.objects.filter(user=candidate.candidate).first()
        profiles.append(profile)
    context = {
        'rec_navbar': 1,
        'profiles': profiles,
        'job': job,
    }
    return render(request, 'staff/candidate_list.html', context)
#----------------------------------------------------------------------------------------
                      #SELECTED LIST
#Contains candidates profiles who have been selected from the candidates list by the staff
@login_required
def selected_list(request, slug):
    job = get_object_or_404(Job, slug=slug)
    selected = Selected.objects.filter(job=job).order_by('date_posted')
    profiles = []
    for candidate in selected:
        profile = Profile.objects.filter(user=candidate.candidate).first()
        profiles.append(profile)
    context = {
        'rec_navbar': 1,
        'profiles': profiles,
        'job': job,
    }
    return render(request, 'staff/selected_list.html', context)
#------------------------------------------------------------------------------------------------
                           #SELECTED CANDIDATE
#Used to select a candidate from the candidates list
# Creates an object for the candidate in the selected list
# Deletes the applicant  from the candidates list after adding it to the selected list               
@login_required
def select_candidate(request, can_id, job_id):
    job = get_object_or_404(Job, slug=job_id)
    profile = get_object_or_404(Profile, slug=can_id)
    user = profile.user
    selected, created = Selected.objects.get_or_create(job=job, candidate=user)
    candidate = Candidates.objects.filter(job=job, candidate=user).first()
    candidate.delete()
    return HttpResponseRedirect('/hiring/job/{}/candidates'.format(job.slug))
#-------------------------------------------------------------------------------------------------
                         #REMOVE CANDIDATE
#Used to reject a candidate who has applied to a particular job post
#Delete the applicant from the candidate list
@login_required
def remove_candidate(request, can_id, job_id):
    job = get_object_or_404(Job, slug=job_id)
    profile = get_object_or_404(Profile, slug=can_id)
    user = profile.user
    candidate = Candidates.objects.filter(job=job, candidate=user).first()
    candidate.delete()
    return HttpResponseRedirect('/hiring/job/{}/candidates'.format(job.slug))
#---------------------------------------------------------------------------------------------
                   