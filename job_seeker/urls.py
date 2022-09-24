from django.urls import path, include
from . import views
#from django.conf.urls.static import static
#from django.conf import settings
#from main.settings import LOGIN_URL, LOGOUT_URL


urlpatterns = [
    path('', views.home, name='home'),
    path('applicant/', views.applicant, name='applicant'),
    path('staff/', views.staff, name='staff'),
    path('profile/', views.my_profile, name='my-profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/staff/', views.RegisterStaff.as_view(), name='register-staff'),
    path('register/applicant/', views.RegisterApplicant.as_view(), name='register-applicant'),
    path('staff/jobs/', views.staff_jobs, name='staff_jobs'),
    path('applicant/applied/', views.applicant_applied, name='applicant_applied'),
    
    path('job/', views.job_search_list, name='job_search_list'),
    path('job/<slug>', views.job_detail, name='job-detail'),
    path('relevant_jobs/', views.intelligent_search, name='intelligent-search'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('profile/<slug>', views.profile_view, name='profile-view'),
    path('delete_skills/', views.delete_skill, name='skill-delete'),
    path('job/<slug>/apply/', views.apply_job, name='apply-job'),
    path('job/<slug>/save/', views.save_job, name='save-job'),
    path('saved_job_list/', views.saved_jobs, name='saved-jobs'),
    path('applied_job_list/', views.applied_jobs, name='applied-jobs'),
    path('job/<slug>/remove/', views.remove_job, name='remove-job'),

]
