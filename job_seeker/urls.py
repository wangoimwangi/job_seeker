from django.urls import path, include
from . import views

urlpatterns = [

                    #USER URLS
    # path('test/', views.test, name='test'),

    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.Services, name='services'),
    path('applicant/', views.applicant, name='applicant'),
    path('staff/', views.staff, name='staff'),
    path('profile/', views.my_profile, name='my-profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/staff/', views.RegisterStaff.as_view(), name='register-staff'),
    path('register/applicant/', views.RegisterApplicant.as_view(), name='register-applicant'),
    #================================================================================================
                          #APPLICANT URLS
    #slug is used to generate valid urls
    path('jobs/', views.posted_jobs, name='posted-jobs'),
    path('jobs/<int:job_id>/', views.job_details, name='job-details'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('delete_skills/', views.delete_skill, name='skill-delete'),
    path('job/<slug>/save/', views.save_job, name='save-job'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply-job'),
    path('saved_job_list/', views.saved_jobs, name='saved-jobs'),
    path('applied_job_list/', views.applied_jobs, name='applied-jobs'),

    #========================================================================================================
                            #STAFF URLS
    path('job/add', views.add_job, name='add-job'),
    path('job/<slug>/edit/', views.edit_job, name='edit-job-post'),
    path('jobs/', views.all_jobs, name='job-list'),
    path('applicant/search/', views.search_applicant, name='search-applicant'),
    path('applications/<int:application_id>/details/', views.application_details, name='applicant-details'),
    path('profile/<slug>', views.profile_view, name='profile-view'),
    path('job/<slug>/search/', views.job_candidate_search, name='job-candidate-search'),

                               #REPORTS
    path('applicants/', views.applied_any_month, name='applied-any-month'),
    path('applicants/<int:month>', views.applied_any_month, name='applied-any-month'),

   


#==============================================================================================================
]





























# path('relevant_jobs/', views.intelligent_search, name='intelligent-search'),
   # path('profile/<slug>', views.profile_view, name='profile-view'),
   # path('job/<slug>/remove/', views.remove_job, name='remove-job'),
   # path('job/<slug>/search/', views.job_applicant_search, name='job-applicant-search'),
   # path('job/<slug>/candidates', views.candidate_list, name='candidate-list'),
   # path('job/<slug>/selected', views.selected_list, name='selected-list'),
   # path('job/<job_id>/select-candidate/<can_id>/', views.select_candidate, name='select-candidate'),
    # path('job/<job_id>>/remove-candidate/<can_id>/', views.remove_candidate, name='remove-candidate'),
