from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Applicant, Staff, Job, Profile, Skill,
    SavedJobs, Application, AppliedJobs, Candidates, Selected
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'full_name', 'email', 'user_type', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('TalentHub Info', {'fields': ('user_type', 'contact', 'location')}),
    )


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['user', 'grad_year', 'job_type']
    list_filter = ['job_type']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'staff', 'date_posted', 'deadline', 'applicant_count']
    list_filter = ['job_type', 'date_posted']
    search_fields = ['title', 'company', 'location', 'description']
    ordering = ['-date_posted']
    readonly_fields = ['date_posted', 'slug']

    def applicant_count(self, obj):
        return obj.application_set.count()
    applicant_count.short_description = 'Applicants'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'location', 'job_type', 'grad_year']
    list_filter = ['job_type']
    search_fields = ['user__username', 'full_name', 'location']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['skill', 'user']
    search_fields = ['skill', 'user__username']
    list_filter = []


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'date_applied', 'status', 'reviewed_by']
    list_filter = ['status', 'date_applied']
    search_fields = ['applicant__user__username', 'applicant__user__first_name', 'job__title']
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
    search_fields = ['user__username', 'job__title']


# Legacy models
admin.site.register(AppliedJobs)
admin.site.register(Candidates)
admin.site.register(Selected)


# Admin site branding
admin.site.site_header = 'TalentHub Administration'
admin.site.site_title = 'TalentHub Admin'
admin.site.index_title = 'Dashboard'
