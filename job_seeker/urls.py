from django.urls import path
from . import views
#from django.conf.urls.static import static
#from django.conf import settings
#from main.settings import LOGIN_URL, LOGOUT_URL



urlpatterns = [
    path('', views.home, name='home'),
    path('applicant/', views.applicant, name='applicant'),
    path('staff/', views.staff, name='staff'),
    
]
