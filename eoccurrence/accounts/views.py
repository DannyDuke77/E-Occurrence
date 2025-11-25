from django.shortcuts import render
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


from .decorators import login_required_with_message

from .models import Userprofile

from .forms import loginForm, CustomUserCreationForm, UserEditForm, UserProfileEditForm

# Create your views here.
@login_required_with_message
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.first_name + ' ' + user.last_name} created successfully. You can now log in.")
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/create user.html', 
                  {'form': form},

                  )

def login_view(request):
    if request.method == 'POST':
        form = loginForm(request, data=request.POST)
        remember_me = request.POST.get("remember_me") == "on"

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")

            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 7)  # 7 days
            else:
                request.session.set_expiry(30 * 60)  # 30 minutes

            return redirect('core:dashboard')
    else:
        form = loginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required_with_message
def profile_view(request, uuid):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view this profile.")
        return redirect('login')

    # Get the profile or return 404 if not found
    profile = get_object_or_404(Userprofile, uuid=uuid)
    user = request.user

    return render(request, 'accounts/profile_view.html', {
        'user': user,
        'profile': profile,
    })

def edit_profile(request, uuid):
    profile = get_object_or_404(Userprofile, uuid=uuid)
    user = profile.user

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile_view', uuid=profile.uuid)
    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileEditForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)
