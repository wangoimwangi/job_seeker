import django_filters
from job_seeker.models import Applicant, Application,Job


class ApplicationFilter(django_filters.FilterSet):
    class Meta:
        model = Application
        fields = ['job', 'applicant', 'date_applied',
                  'approved', 'approved_by', 'date_approved']
