"""Custom decorators for access control."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=[]):
    """Restrict view to users with specific roles."""
    def decorator(view_func):
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.profile.role == 'admin' or request.user.profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard:home')
        return _wrapped
    return decorator