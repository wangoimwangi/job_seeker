from django.shortcuts import redirect
from django.contrib import messages
from .models import User


def staff_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.user_type == User.STAFF or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access denied. This page is for employers only.')
        return redirect('home')
    wrapper_func.__name__ = view_func.__name__
    return wrapper_func


def applicant_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.user_type == User.APPLICANT:
            return view_func(request, *args, **kwargs)
        if request.user.user_type == User.STAFF:
            return redirect('staff')
        messages.error(request, 'Access denied. This page is for job seekers only.')
        return redirect('home')
    wrapper_func.__name__ = view_func.__name__
    return wrapper_func
