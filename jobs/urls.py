from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from job_seeker import views as jv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('job_seeker.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'job_seeker.views.handler404'
handler500 = 'job_seeker.views.handler500'
