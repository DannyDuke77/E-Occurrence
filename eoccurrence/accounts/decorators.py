# accounts/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required_with_message(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper