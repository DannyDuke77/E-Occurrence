from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def terms(request):
    return render(request, 'core/terms of use.html')