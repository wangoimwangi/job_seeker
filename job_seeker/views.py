from ast import Return
#from multiprocessing import context
#from jobs. jobs.job_seeker.models import Applicant
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here
def home(request):
    return render(request, 'jobseeker/home.html')
    
def applicant(request):
    return render(request, 'applicant/applicant.html')

def staff(request):
    #applicants = Applicant.objects.all()
    #context = {
        #'applicants': applicants
    #}
    return render(request, 'staff/staff.html') #,context)


