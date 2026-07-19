"""Authentication views: login, logout, profile, password change, user management."""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from .forms import (
    StyledAuthenticationForm,
    UserProfileForm,
    StyledPasswordChangeForm,
    ForgotPasswordForm,
    CustomUserCreationForm,
    CustomUserEditForm,
)
from .models import ActivityLog, UserProfile
from core.decorators import role_required


@never_cache
def login_view(request):
    """Custom styled login view."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = StyledAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            ActivityLog.objects.create(
                user=user, action='login', module='accounts',
                description=f'{user.username} logged in',
            )
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            next_url = request.GET.get('next') or 'dashboard:home'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = StyledAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@never_cache
@login_required
def logout_view(request):
    """Logout view."""
    ActivityLog.objects.create(
        user=request.user, action='logout', module='accounts',
        description=f'{request.user.username} logged out',
    )
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')


@login_required
def profile_view(request):
    """View and edit user profile."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(
                user=request.user, action='update', module='accounts',
                description='Updated profile information',
            )
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password_view(request):
    """Change password view."""
    if request.method == 'POST':
        form = StyledPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StyledPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


def forgot_password_view(request):
    """Forgot password view (template ready)."""
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            messages.info(request, 'If an account exists with that email, a reset link has been sent.')
            return redirect('accounts:login')
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})


# ==========================================
# USER MANAGEMENT VIEWS
# ==========================================

@role_required(['admin'])
def user_list(request):
    """List all system users."""
    users = User.objects.select_related('profile').all().order_by('date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@role_required(['admin'])
def user_create(request):
    """Create a new system user."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign role to profile
            user.profile.role = form.cleaned_data.get('role')
            user.profile.save()
            ActivityLog.objects.create(
                user=request.user, action='create', module='accounts',
                description=f'Created user: {user.username} ({user.profile.role})',
            )
            messages.success(request, 'User created successfully.')
            return redirect('accounts:user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Add User'})


@role_required(['admin'])
def user_update(request, pk):
    """Edit an existing system user."""
    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=target_user)
        if form.is_valid():
            user = form.save()
            user.profile.role = form.cleaned_data.get('role')
            user.profile.save()
            ActivityLog.objects.create(
                user=request.user, action='update', module='accounts',
                description=f'Updated user: {user.username}',
            )
            messages.success(request, 'User updated successfully.')
            return redirect('accounts:user_list')
    else:
        form = CustomUserEditForm(instance=target_user, initial={'role': target_user.profile.role})
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Edit User', 'target_user': target_user})


@role_required(['admin'])
def user_delete(request, pk):
    """Delete a system user."""
    target_user = get_object_or_404(User, pk=pk)
    if target_user == request.user:
        messages.error(request, 'You cannot delete your own account!')
        return redirect('accounts:user_list')
    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        ActivityLog.objects.create(
            user=request.user, action='delete', module='accounts',
            description=f'Deleted user: {username}',
        )
        messages.success(request, f'User "{username}" deleted.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_confirm_delete.html', {'target_user': target_user})