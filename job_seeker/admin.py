from django.contrib import admin

# Register your models here
from .models import *
admin.site.register(User)
admin.site.register(Applicant)
admin.site.register(Staff)
admin.site.register(JobCategory)
admin.site.register( Job)
admin.site.register(JobApplication)


