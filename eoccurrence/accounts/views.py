from django.shortcuts import render
from django.contrib.auth import login, logout
from django.shortcuts import redirect

from .forms import CustomUserCreationForm

# Create your views here.
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts/login/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/create user.html', 
                  {'form': form},

                  )

def logout_view(request):
    logout(request)
    return redirect('/')