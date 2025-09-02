from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import User
from django.contrib import messages

from django.core.paginator import Paginator

from .models import SupportRequest

from .forms import SupportRequestForm

from accounts.models import Userprofile

from cases.models import Case, CourtDecision

from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def dashboard(request):
    return render(request, 'core/dashboard.html')

def terms_of_use(request):
    return render(request, 'core/terms of use.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def faq(request):
    return render(request, 'core/faq.html')

def help_support(request):
    if request.method == 'POST':
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent! Our team will get back to you as soon as possible.")
            return redirect('core:help_support')  # reload page after success
    else:
        form = SupportRequestForm()

    return render(request, 'core/help_support.html', {'form': form})

# Only allow staff/admin users to access
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def admin_dashboard(request):
    if not request.user.is_staff or not request.user.is_superuser:
            messages.error(request, "You do not have permission to view this page.")
            return redirect('core:dashboard')
    
    # Quick stats
    total_users = User.objects.count()
    active_users = Userprofile.objects.filter(is_active=True).count()
    open_cases = Case.objects.filter(status="open").count()
    closed_cases = Case.objects.filter(status="closed").count()
    pending_support = SupportRequest.objects.filter(status="pending").count()
    court_decisions = CourtDecision.objects.count()

    # Recent activity
    recent_cases = Case.objects.order_by("-created_at")[:5]
    recent_decisions = CourtDecision.objects.order_by("-decision_date")[:5]
    recent_support = SupportRequest.objects.order_by("-created_at")[:5]
    recent_users = User.objects.order_by("-date_joined")[:5]

    context = {
        # Quick stats
        "total_users": total_users,
        "active_users": active_users,
        "open_cases": open_cases,
        "closed_cases": closed_cases,
        "pending_support": pending_support,
        "court_decisions": court_decisions,

        # Recent activity
        "recent_cases": recent_cases,
        "recent_decisions": recent_decisions,
        "recent_support": recent_support,
        "recent_users": recent_users,
    }

    return render(request, "core/admin_dashboard.html", context)

def support_requests_list(request):
    requests = SupportRequest.objects.all().order_by('-created_at')
    
    # Paginate — display 10 per page
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/support_requests_list.html', {'page_obj': page_obj})

def support_request_detail(request, uuid):
    req = get_object_or_404(SupportRequest, uuid=uuid)

    return render(request, 'core/support_request_detail.html', {'req': req})
