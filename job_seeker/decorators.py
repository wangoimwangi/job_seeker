from django.http.response import HttpResponse

from .models import User


def staff_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.user_type == User.STAFF:
            return view_func(request, *args, **kwargs)
        else:
            error_msg = 'Unauthorised action. You must be a staff to access this page!'
            return HttpResponse(error_msg)
    return wrapper_func

def applicant_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.user_type == User.APPLICANT:
            return view_func(request, *args, **kwargs)
        else:
            error_msg = 'Unauthorised action. You must be a staff to access this page!'
            return HttpResponse(error_msg)
    return wrapper_func
