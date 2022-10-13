from django.urls import path, include
from . import views

urlpatterns = [
                    #USER URLS
    path('', views.home, name='home'),
    path('applicant/', views.applicant, name='applicant'),
    path('staff/', views.staff, name='staff'),
    #path('job/', views.job, name='job'),
    path('profile/', views.my_profile, name='my-profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/staff/', views.RegisterStaff.as_view(), name='register-staff'),
    path('register/applicant/', views.RegisterApplicant.as_view(), name='register-applicant'),
    #================================================================================================
                          #APPLICANT URLS

    #slug is used to generate valid urls
    path('job/', views.job_search_list, name='job-search-list'),
    path('jobs/', views.posted_jobs, name='posted-jobs'),
    path('jobs/<int:job_id>/', views.job_details, name='job-details'),
    path('relevant_jobs/', views.intelligent_search, name='intelligent-search'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('profile/<slug>', views.profile_view, name='profile-view'),
    path('delete_skills/', views.delete_skill, name='skill-delete'),
    path('job/<slug>/apply/', views.apply_job, name='apply-job'),
    path('job/<slug>/save/', views.save_job, name='save-job'),
    path('saved_job_list/', views.saved_jobs, name='saved-jobs'),
    path('applied_job_list/', views.applied_jobs, name='applied-jobs'),
    path('job/<slug>/remove/', views.remove_job, name='remove-job'),
    #========================================================================================================
                            #STAFF URLS

    path('job/add', views.add_job, name='add-job'),
    path('job/<slug>/edit/', views.edit_job, name='edit-job-post'),
    # path('job/<slug>', views.job_detail, name='add-job-detail'),
    path('jobs/', views.all_jobs, name='job-list'),
    path('applicant/search/', views.search_applicant, name='search-applicant'),
    path('job/<slug>/search/', views.job_applicant_search, name='job-applicant-search'),
    path('job/<slug>/candidates', views.candidate_list, name='candidate-list'),
    path('job/<slug>/selected', views.selected_list, name='selected-list'),
    path('job/<job_id>/select-candidate/<can_id>/', views.select_candidate, name='select-candidate'),
    path('job/<job_id>>/remove-candidate/<can_id>/', views.remove_candidate, name='remove-candidate'),
#==============================================================================================================
]
