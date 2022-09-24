from django.contrib import admin

# Register your models here
from .models import *
admin.site.register(User)
admin.site.register(Applicant)
admin.site.register(Staff)
admin.site.register( Job)
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(SavedJobs)
admin.site.register(AppliedJobs)
admin.site.register(Candidates)
admin.site.register(Selected)



