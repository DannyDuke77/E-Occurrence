# accounts/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """
    Decorator to restrict access to users with role='admin' in UserProfile.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            # Redirect to login page if not authenticated
            return redirect('login')

        # Check if the user has a profile and role is admin
        profile = getattr(user, 'userprofile', None)
        if profile is None or profile.user_role != 'admin':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('error_404')

        return view_func(request, *args, **kwargs)

    return _wrapped_view
