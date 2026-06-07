import datetime as DT
import calendar as CAL
import pytz

from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count

from .models import (
    User, Applicant, Staff, Job, Profile, Skill,
    SavedJobs, Application, AppliedJobs, APPLICATION_STATUS
)
from .forms import (
    StaffRegistrationForm, ApplicantRegistrationForm,
    ProfileUpdateForm, NewSkillForm, NewJobForm, JobApplicationForm
)
from .decorators import staff_required, applicant_required

utc = pytz.UTC


# ─── Home ───────────────────────────────────────────────────────────────────

def home(request):
    featured_jobs = Job.objects.order_by('-date_posted')[:3]
    total_jobs = Job.objects.count()
    total_applicants = Applicant.objects.count()
    context = {
        'featured_jobs': featured_jobs,
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
    }
    return render(request, 'jobseeker/home.html', context)


def contact(request):
    return render(request, 'jobseeker/contact.html')


def services(request):
    return render(request, 'jobseeker/services.html')


# ─── Authentication ──────────────────────────────────────────────────────────

def user_login(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    if request.method != 'POST':
        form = AuthenticationForm()
        return render(request, 'jobseeker/login.html', {'form': form})

    form = AuthenticationForm(data=request.POST)
    if not form.is_valid():
        messages.error(request, 'Invalid username or password. Please try again.')
        return render(request, 'jobseeker/login.html', {'form': form})

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)

    if user is None:
        messages.error(request, 'Authentication failed. Please check your credentials.')
        return render(request, 'jobseeker/login.html', {'form': form})

    # Handle "remember me"
    if not request.POST.get('remember'):
        request.session.set_expiry(0)
    else:
        request.session.set_expiry(1800)  # 30 minutes

    login(request, user)
    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
    return _redirect_by_role(user)


def _redirect_by_role(user):
    if user.is_superuser or user.is_staff:
        return redirect('/admin/')
    if user.user_type == User.APPLICANT:
        return redirect('applicant')
    if user.user_type == User.STAFF:
        return redirect('staff')
    return redirect('home')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# ─── Registration ────────────────────────────────────────────────────────────

def register(request):
    return render(request, 'jobseeker/register.html')


class RegisterStaff(CreateView):
    form_class = StaffRegistrationForm
    template_name = 'staff/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('staff')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created! Welcome to TalentHub.')
        return redirect('staff')

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class RegisterApplicant(CreateView):
    form_class = ApplicantRegistrationForm
    template_name = 'applicant/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('applicant')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        # Create a blank profile for the applicant
        Profile.objects.get_or_create(user=user)
        login(self.request, user)
        messages.success(self.request, 'Account created! Please complete your profile.')
        return redirect('applicant')

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


# ─── Applicant Dashboard ─────────────────────────────────────────────────────

@login_required
@applicant_required
def applicant_dashboard(request):
    user = request.user
    applications = Application.objects.filter(applicant__user=user).select_related('job')
    saved = SavedJobs.objects.filter(user=user)
    profile = Profile.objects.filter(user=user).first()

    hour = DT.datetime.now().hour
    if hour < 12:
        greeting = 'Good morning'
    elif hour < 17:
        greeting = 'Good afternoon'
    else:
        greeting = 'Good evening'

    recent_applications = applications[:5]
    recommended_jobs = Job.objects.exclude(
        id__in=applications.values_list('job_id', flat=True)
    ).order_by('-date_posted')[:3]

    context = {
        'greeting': greeting,
        'applied_count': applications.count(),
        'saved_count': saved.count(),
        'total_jobs': Job.objects.count(),
        'recent_applications': recent_applications,
        'recommended_jobs': recommended_jobs,
        'profile': profile,
        'profile_complete': profile.completion_percentage() if profile else 0,
    }
    return render(request, 'applicant/applicant.html', context)


# ─── Profile ─────────────────────────────────────────────────────────────────

@login_required
def my_profile(request):
    user = request.user

    if user.user_type == User.STAFF:
        context = {
            'u': user,
            'jobs_count': Job.objects.filter(staff=user).count(),
            'applications_count': Application.objects.filter(job__staff=user).count(),
        }
        return render(request, 'staff/staff_profile.html', context)

    profile, _ = Profile.objects.get_or_create(user=user)
    skills = Skill.objects.filter(user=user)

    if request.method == 'POST':
        form = NewSkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = user
            skill.save()
            messages.success(request, 'Skill added successfully.')
            return redirect('my-profile')
    else:
        form = NewSkillForm()

    context = {
        'u': user,
        'profile': profile,
        'skills': skills,
        'form': form,
        'completion': profile.completion_percentage(),
    }
    return render(request, 'applicant/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user

    if user.user_type == User.STAFF:
        if request.method == 'POST':
            full_name = request.POST.get('full_name', '').strip()
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
            user.location = request.POST.get('location', '').strip()
            user.contact = request.POST.get('contact', '').strip()
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('my-profile')
        return render(request, 'staff/staff_edit_profile.html', {'u': user})

    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('my-profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial = {}
        if not profile.full_name:
            initial['full_name'] = request.user.get_full_name()
        if not profile.location:
            initial['location'] = request.user.location
        form = ProfileUpdateForm(instance=profile, initial=initial)

    return render(request, 'applicant/edit_profile.html', {'form': form, 'profile': profile})


@login_required
def profile_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    skills = Skill.objects.filter(user=profile.user)
    applications = Application.objects.filter(applicant__user=profile.user)
    context = {
        'u': profile.user,
        'profile': profile,
        'skills': skills,
        'applications': applications,
    }
    return render(request, 'applicant/profile.html', context)


@login_required
@staff_required
def staff_view_applicant_profile(request, user_id):
    applicant_user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.filter(user=applicant_user).first()
    skills = Skill.objects.filter(user=applicant_user)
    applications = Application.objects.filter(
        applicant__user=applicant_user
    ).select_related('job').order_by('-date_applied')
    context = {
        'applicant_user': applicant_user,
        'profile': profile,
        'skills': skills,
        'applications': applications,
    }
    return render(request, 'staff/applicant_profile_view.html', context)


@login_required
@csrf_exempt
def delete_skill(request, pk=None):
    if request.method == 'POST':
        id_list = request.POST.getlist('choices')
        for skill_id in id_list:
            try:
                skill = Skill.objects.get(id=skill_id, user=request.user)
                skill.delete()
            except Skill.DoesNotExist:
                pass
        messages.success(request, 'Skill(s) removed.')
        return redirect('my-profile')
    return redirect('my-profile')


# ─── Jobs (Applicant) ────────────────────────────────────────────────────────

def posted_jobs(request):
    jobs = Job.objects.all().order_by('-date_posted')

    # Search and filter
    search_query = request.GET.get('q', '').strip()
    location_filter = request.GET.get('location', '').strip()
    job_type_filter = request.GET.get('job_type', '').strip()

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(skills_req__icontains=search_query) |
            Q(company__icontains=search_query)
        )
    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)
    if job_type_filter:
        jobs = jobs.filter(job_type=job_type_filter)

    # Build applied IDs set for current applicant
    applied_ids = set()
    saved_ids = set()
    if request.user.is_authenticated and request.user.user_type == User.APPLICANT:
        applied_ids = set(
            Application.objects.filter(applicant__user=request.user)
            .values_list('job_id', flat=True)
        )
        saved_ids = set(
            SavedJobs.objects.filter(user=request.user)
            .values_list('job_id', flat=True)
        )

    paginator = Paginator(jobs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Get distinct locations for filter dropdown
    locations = Job.objects.values_list('location', flat=True).distinct().order_by('location')

    context = {
        'page_obj': page_obj,
        'jobs': page_obj,
        'applied_ids': applied_ids,
        'saved_ids': saved_ids,
        'total_count': jobs.count(),
        'search_query': search_query,
        'location_filter': location_filter,
        'job_type_filter': job_type_filter,
        'job_types': ['Full Time', 'Part Time', 'Internship'],
        'locations': locations,
    }
    return render(request, 'jobseeker/posted_jobs.html', context)


def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    already_applied = False
    is_saved = False

    if request.user.is_authenticated:
        if request.user.user_type == User.APPLICANT:
            already_applied = Application.objects.filter(
                applicant__user=request.user, job=job
            ).exists()
            is_saved = SavedJobs.objects.filter(user=request.user, job=job).exists()

    # Similar jobs (same job type, exclude current)
    similar_jobs = Job.objects.filter(job_type=job.job_type).exclude(id=job_id).order_by('-date_posted')[:3]

    # Staff sees applicants
    applications = None
    if request.user.is_authenticated and request.user.user_type == User.STAFF:
        applications = Application.objects.filter(job=job).select_related('applicant__user')

    context = {
        'job': job,
        'already_applied': already_applied,
        'is_saved': is_saved,
        'similar_jobs': similar_jobs,
        'applications': applications,
        'skills_list': job.get_skills_list(),
    }
    return render(request, 'jobseeker/job_detail.html', context)


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check already applied
    if Application.objects.filter(applicant__user=request.user, job=job).exists():
        messages.info(request, 'You have already applied for this job.')
        return redirect('job-details', job_id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                applicant = request.user.applicant
            except Applicant.DoesNotExist:
                messages.error(request, 'Your applicant profile is not set up. Please contact support.')
                return redirect('my-profile')

            application = form.save(commit=False)
            application.job = job
            application.applicant = applicant
            application.date_applied = DT.datetime.now()
            application.save()
            messages.success(request, f'Your application for "{job.title}" has been submitted!')
            return redirect('applied-jobs')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobApplicationForm()

    profile = Profile.objects.filter(user=request.user).first()
    context = {'form': form, 'job': job, 'profile': profile}
    return render(request, 'applicant/apply.html', context)


@login_required
def save_job(request, slug):
    job = get_object_or_404(Job, slug=slug)
    saved, created = SavedJobs.objects.get_or_create(job=job, user=request.user)
    if created:
        messages.success(request, f'"{job.title}" saved to your list.')
    else:
        saved.delete()
        messages.info(request, f'"{job.title}" removed from your saved jobs.')
    # Redirect back to where we came from
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(next_url)


@login_required
def saved_jobs(request):
    jobs = SavedJobs.objects.filter(user=request.user).order_by('-date_posted').select_related('job')
    applied_ids = set(
        Application.objects.filter(applicant__user=request.user)
        .values_list('job_id', flat=True)
    )
    context = {'jobs': jobs, 'applied_ids': applied_ids}
    return render(request, 'applicant/saved_jobs.html', context)


@login_required
def applied_jobs(request):
    applications = Application.objects.filter(
        applicant__user=request.user
    ).select_related('job').order_by('-date_applied')
    context = {'applications': applications}
    return render(request, 'applicant/applied_jobs.html', context)


@login_required
def withdraw_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(
            Application,
            id=application_id,
            applicant=request.user.applicant
        )
        if application.status == 'pending':
            application.delete()
            messages.success(request, 'Application withdrawn successfully.')
        else:
            messages.error(request, 'Only pending applications can be withdrawn.')
    return redirect('applied-jobs')


# ─── Staff Dashboard ──────────────────────────────────────────────────────────

@login_required
@staff_required
def staff_dashboard(request):
    user = request.user
    my_jobs = Job.objects.filter(staff=user)
    total_applicants = Application.objects.filter(job__staff=user).count()
    pending = Application.objects.filter(job__staff=user, status='pending').count()

    recent_applications = Application.objects.filter(
        job__staff=user
    ).select_related('job', 'applicant__user').order_by('-date_applied')[:10]

    context = {
        'active_jobs': my_jobs.count(),
        'total_applicants': total_applicants,
        'pending_reviews': pending,
        'profile_views': 0,
        'recent_applications': recent_applications,
        'my_jobs': my_jobs[:5],
    }
    return render(request, 'staff/staff.html', context)


@login_required
@staff_required
def add_job(request):
    if request.method == 'POST':
        form = NewJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.staff = request.user
            job.save()
            messages.success(request, f'Job "{job.title}" posted successfully.')
            return redirect('job-list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewJobForm()

    return render(request, 'staff/add_job.html', {'form': form})


@login_required
@staff_required
def edit_job(request, slug):
    job = get_object_or_404(Job, slug=slug, staff=request.user)

    if request.method == 'POST':
        form = NewJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('job-details', job_id=job.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewJobForm(instance=job)

    return render(request, 'staff/edit_jobs.html', {'form': form, 'job': job})


@login_required
@staff_required
def delete_job(request, slug):
    job = get_object_or_404(Job, slug=slug, staff=request.user)
    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f'Job "{title}" deleted.')
        return redirect('job-list')
    return render(request, 'staff/confirm_delete.html', {'job': job})


@login_required
@staff_required
def all_jobs(request):
    jobs = Job.objects.filter(staff=request.user).annotate(
        app_count=Count('application')
    ).order_by('-date_posted')

    search_query = request.GET.get('q', '').strip()
    if search_query:
        jobs = jobs.filter(Q(title__icontains=search_query) | Q(location__icontains=search_query))

    paginator = Paginator(jobs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {'jobs': page_obj, 'search_query': search_query, 'today': DT.date.today()}
    return render(request, 'staff/job_post.html', context)


@login_required
@staff_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, staff=request.user)
    applications = Application.objects.filter(job=job).select_related(
        'applicant__user'
    ).order_by('-date_applied')
    context = {'job': job, 'applications': applications}
    return render(request, 'staff/job_applicants.html', context)


@login_required
@staff_required
def application_details(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__staff=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        status_map = {
            'shortlist': 'shortlisted',
            'reject': 'rejected',
            'process': 'in_process',
        }
        if action in status_map:
            application.status = status_map[action]
            application.reviewed_by = request.user.staff
            application.date_reviewed = DT.datetime.now()
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}.')
        return redirect('job-applicants', job_id=application.job.id)

    profile = Profile.objects.filter(user=application.applicant.user).first()
    skills = Skill.objects.filter(user=application.applicant.user)
    all_applications = Application.objects.filter(
        applicant=application.applicant
    ).select_related('job').order_by('-date_applied')
    context = {
        'application': application,
        'profile': profile,
        'skills': skills,
        'all_applications': all_applications,
    }
    return render(request, 'staff/application-details.html', context)


@login_required
@staff_required
def search_applicant(request):
    profiles = Profile.objects.exclude(user=request.user).select_related('user')

    location_q = request.GET.get('r', '').strip()
    job_type_q = request.GET.get('s', '').strip()

    if location_q:
        profiles = profiles.filter(location__icontains=location_q)
    if job_type_q:
        profiles = profiles.filter(job_type=job_type_q)

    # Only show profiles with resumes
    profiles = [p for p in profiles if p.resume]

    paginator = Paginator(profiles, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Reports: applications per selected month
    month = request.GET.get('month')
    app_count = 0
    selected_month = None
    if month:
        try:
            month = int(month)
            today = DT.datetime.now()
            x_month_range = CAL.monthrange(today.year, month)
            x_month_start = DT.datetime(today.year, month, 1, tzinfo=utc)
            x_month_end = DT.datetime(today.year, month, x_month_range[1], 23, 59, 59, tzinfo=utc)
            app_count = Application.objects.filter(
                date_applied__gte=x_month_start,
                date_applied__lte=x_month_end
            ).count()
            selected_month = month
        except (ValueError, TypeError):
            pass

    months = [(i, DT.date(2000, i, 1).strftime('%B')) for i in range(1, 13)]

    context = {
        'profiles': page_obj,
        'location_q': location_q,
        'job_type_q': job_type_q,
        'job_types': ['Full Time', 'Part Time', 'Internship'],
        'app_count': app_count,
        'selected_month': selected_month,
        'months': months,
    }
    return render(request, 'staff/applicant_search.html', context)


@login_required
@staff_required
def job_candidate_search(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job_skills = [s.strip().lower() for s in (job.skills_req or '').split(',') if s.strip()]

    relevant_candidates = []
    applicants = Profile.objects.filter(job_type=job.job_type).select_related('user')

    for applicant in applicants:
        user_skills = [s.skill.lower() for s in Skill.objects.filter(user=applicant.user)]
        common = list(set(job_skills) & set(user_skills))
        if common and len(common) >= max(1, len(job_skills) // 2):
            relevant_candidates.append((applicant, len(common)))

    relevant_candidates.sort(key=lambda x: x[1], reverse=True)

    context = {
        'job': job,
        'objects': relevant_candidates[:100],
        'job_skills': len(job_skills),
        'relevant': len(relevant_candidates),
    }
    return render(request, 'staff/job_applicant_search.html', context)


def applied_any_month(request, month=None):
    today = DT.datetime.now()
    if not month:
        month = today.month

    try:
        month = int(month)
        x_month_range = CAL.monthrange(today.year, month)
        x_month_start = DT.datetime(today.year, month, 1, tzinfo=utc)
        x_month_end = DT.datetime(today.year, month, x_month_range[1], 23, 59, 59, tzinfo=utc)
        count = Application.objects.filter(
            date_applied__gte=x_month_start,
            date_applied__lte=x_month_end
        ).count()
    except (ValueError, TypeError):
        count = 0
        month = today.month

    months = [(i, DT.date(2000, i, 1).strftime('%B')) for i in range(1, 13)]

    status_counts = {}
    top_jobs = []
    if request.user.is_authenticated and request.user.user_type == User.STAFF:
        staff_apps = Application.objects.filter(job__staff=request.user)
        status_counts = {
            'pending': staff_apps.filter(status='pending').count(),
            'in_process': staff_apps.filter(status='in_process').count(),
            'shortlisted': staff_apps.filter(status='shortlisted').count(),
            'rejected': staff_apps.filter(status='rejected').count(),
        }
        top_jobs = Job.objects.filter(staff=request.user).annotate(
            app_count=Count('application')
        ).order_by('-app_count')[:5]

    context = {
        'count': count,
        'selected_month': month,
        'months': months,
        'status_counts': status_counts,
        'top_jobs': top_jobs,
        'today': DT.date.today(),
    }
    return render(request, 'staff/all_months.html', context)


# ─── Error pages ──────────────────────────────────────────────────────────────

def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
