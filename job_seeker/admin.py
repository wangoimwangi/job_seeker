import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Applicant, Staff, Job, Profile, Skill,
    SavedJobs, Application, AppliedJobs, Candidates, Selected
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'user_type', 'is_active']
    list_filter = ['user_type', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('TalentHub Info', {'fields': ('user_type', 'contact', 'location')}),
    )


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'grad_year', 'job_type']
    list_filter = ['job_type']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']

    def location(self, obj):
        return obj.user.location or '-'
    location.short_description = 'Location'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'location']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']

    def location(self, obj):
        return obj.user.location or '-'
    location.short_description = 'Location'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'status', 'date_posted']
    list_filter = ['job_type', 'date_posted']
    search_fields = ['title', 'company', 'location']
    ordering = ['-date_posted']
    readonly_fields = ['date_posted', 'slug']

    def status(self, obj):
        if obj.deadline and obj.deadline < datetime.date.today():
            return 'Closed'
        return 'Active'
    status.short_description = 'Status'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'grad_year', 'job_type']
    list_filter = ['job_type']
    search_fields = ['user__first_name', 'user__last_name', 'location']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['skill', 'user']
    search_fields = ['skill', 'user__first_name', 'user__last_name']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'date_applied', 'status', 'reviewed_by']
    list_filter = ['status', 'date_applied']
    search_fields = ['applicant__user__first_name', 'applicant__user__last_name', 'job__title']
    ordering = ['-date_applied']
    readonly_fields = ['date_applied']

    actions = ['mark_shortlisted', 'mark_rejected', 'mark_in_process']

    def mark_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
    mark_shortlisted.short_description = 'Mark selected as Shortlisted'

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = 'Mark selected as Rejected'

    def mark_in_process(self, request, queryset):
        queryset.update(status='in_process')
    mark_in_process.short_description = 'Mark selected as In Process'


@admin.register(SavedJobs)
class SavedJobsAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'date_posted']
    search_fields = ['user__username', 'user__first_name', 'job__title']


@admin.register(AppliedJobs)
class AppliedJobsAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'date_posted']
    search_fields = ['user__username', 'job__title']


@admin.register(Candidates)
class CandidatesAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'date_posted']
    search_fields = ['candidate__username', 'candidate__first_name', 'job__title']


@admin.register(Selected)
class SelectedAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'date_posted']
    search_fields = ['candidate__username', 'candidate__first_name', 'job__title']


# Admin site branding
admin.site.site_header = 'TalentHub Administration'
admin.site.site_title = 'TalentHub Admin'
admin.site.index_title = 'Dashboard'
