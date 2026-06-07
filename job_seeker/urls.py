from django.urls import path
from . import views

urlpatterns = [
    # ── Public ──────────────────────────────────────────────────────────────
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/staff/', views.RegisterStaff.as_view(), name='register-staff'),
    path('register/applicant/', views.RegisterApplicant.as_view(), name='register-applicant'),

    # ── Jobs (public browse) ─────────────────────────────────────────────────
    path('jobs/', views.posted_jobs, name='posted-jobs'),
    path('jobs/<int:job_id>/', views.job_details, name='job-details'),

    # ── Applicant ────────────────────────────────────────────────────────────
    path('applicant/', views.applicant_dashboard, name='applicant'),
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('profile/<slug:slug>/', views.profile_view, name='profile-view'),
    path('delete-skills/', views.delete_skill, name='skill-delete'),
    path('job/<slug:slug>/save/', views.save_job, name='save-job'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply-job'),
    path('saved-jobs/', views.saved_jobs, name='saved-jobs'),
    path('applied-jobs/', views.applied_jobs, name='applied-jobs'),
    path('application/<int:application_id>/withdraw/', views.withdraw_application, name='withdraw-application'),

    # ── Staff ─────────────────────────────────────────────────────────────────
    path('staff/', views.staff_dashboard, name='staff'),
    path('staff/jobs/', views.all_jobs, name='job-list'),
    path('staff/jobs/add/', views.add_job, name='add-job'),
    path('staff/jobs/<slug:slug>/edit/', views.edit_job, name='edit-job-post'),
    path('staff/jobs/<slug:slug>/delete/', views.delete_job, name='delete-job'),
    path('staff/jobs/<int:job_id>/applicants/', views.job_applicants, name='job-applicants'),
    path('staff/applications/<int:application_id>/', views.application_details, name='applicant-details'),
    path('staff/applicants/', views.search_applicant, name='search-applicant'),
    path('staff/applicant/<int:user_id>/profile/', views.staff_view_applicant_profile, name='staff-applicant-profile'),
    path('staff/jobs/<slug:slug>/search/', views.job_candidate_search, name='job-candidate-search'),

    # ── Reports ───────────────────────────────────────────────────────────────
    path('staff/reports/', views.applied_any_month, name='applied-any-month'),
    path('staff/reports/<int:month>/', views.applied_any_month, name='applied-any-month-filter'),
]
