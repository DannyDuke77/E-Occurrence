from django.shortcuts import render
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from .forms import loginForm

from django.contrib import messages


from .forms import CustomUserCreationForm

# Create your views here.
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.first_name + ' ' + user.last_name} created successfully. You can now log in.")
            return redirect('/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/create user.html', 
                  {'form': form},

                  )

def login_view(request):
    if request.method == 'POST':
        form = loginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('/')  # Redirect to homepage
        else:
            # Handle non-field errors from the form (invalid login or inactive)
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = loginForm()
    
    return render(request, 'accounts/login.html', 
                  {'form': form}
                  )

def logout_view(request):
    logout(request)
    return redirect('/')