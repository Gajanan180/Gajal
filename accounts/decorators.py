from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import User


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.is_superuser or request.user.role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return wrapper
    return decorator


def merchant_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_merchant or request.user.is_superuser):
            messages.error(request, 'Merchant access only.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def customer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_customer or request.user.is_superuser):
            messages.error(request, 'Customer access only.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
