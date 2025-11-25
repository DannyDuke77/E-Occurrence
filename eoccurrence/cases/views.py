from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import CharField, Value
from django.core.paginator import Paginator
import datetime
from django.utils import timezone

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .forms import ComplainantForm, CaseForm, WitnessForm,  SuspectForm, CourtDecisionForm, SuspectCourtRulingForm, CaseForm
from .models import Complainant, Case, Suspect, Witness, CourtDecision, SuspectCourtRuling

from accounts.decorators import login_required_with_message

from accounts.models import Userprofile

@login_required_with_message
def complainant_entry(request):
    if request.method == 'POST':
        form = ComplainantForm(request.POST)
        if form.is_valid():
            complainant = form.save()
            return redirect('cases:case_entry', uuid=complainant.uuid)
    else:
        form = ComplainantForm()

    return render(request, 'cases/complainant_entry.html', {'form': form})

@login_required_with_message
def case_entry(request, uuid):
    complainant = get_object_or_404(Complainant, uuid=uuid)
    form_title = f"New Case for {complainant.first_name} {complainant.last_name}"
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.complainant = complainant
            case.recorded_by = request.user
            case.save()

            name = complainant.first_name
            if complainant.last_name:
                name += f" {complainant.last_name}"

            messages.success(request, f"Case {case.case_number} created successfully for {name}.")
            return redirect("cases:case_details", uuid=case.uuid)  # or any success page
    else:
        form = CaseForm()

    return render(request, 'cases/case_entry.html', {
        'form_title': form_title,
        'form': form,
        'complainant': complainant
    })

def view_cases(request):
    if request.user.is_authenticated and request.user.profile.user_role == 'admin':
        qs = Case.objects.all().filter().order_by('-created_at')
    else:
        qs = Case.objects.all().filter(deleted=False).order_by('-created_at')

    total_results = qs.count()

    # Limit to 20 for performance
    cases = qs[:20]

    # Let user know if results are capped
    if total_results > 20:
        messages.info(request, f"Showing only 20 of {total_results} cases. Please use search to refine results.")

    return render(request, 'cases/view_cases.html', {
        'cases': cases,
        'total_results': total_results,  # pass count to template
    })

@login_required_with_message
def edit_case(request, uuid):
    user = request.user
    case = get_object_or_404(Case, uuid=uuid)
    if case.deleted:
        messages.error(request, "This case has been deleted.")
        return redirect('cases:view_cases')
    
    form_title = f"Edit Case #{ case.case_number }"
    complainant = case.complainant

    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Case {case.case_number} updated successfully.")
            return redirect('cases:case_details', uuid=case.uuid)
    else:
        form = CaseForm(instance=case)

    return render(request, 'cases/case_entry.html', {
        'form_title': form_title,
        'form': form,
        'case': case,
        'complainant': complainant
    })

@login_required_with_message
def case_details(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)
    if case.deleted and not request.user.profile.user_role == 'admin':
        messages.error(request, f"Access denied. You do not have permission to view this case.")
        return redirect('cases:view_cases')
    
    witnesses = case.witnesses.all()
    suspects = case.suspects.all()
    court_decisions = case.court_decisions.all().order_by('decision_date')
    
    return render(request, "cases/case_details.html", {
        "case": case,
        "witnesses": witnesses,
        "suspects": suspects,
        "court_decisions": court_decisions
    })

    
def search_cases(request):
    query = request.GET.get('query', '').strip()
    status = request.GET.get('status', '')
    recorded_by = request.GET.get('recorded_by', '')

    cases = Case.objects.all().filter(deleted=False)

    result_name = "cases"

    if status:
        cases = cases.filter(status=status)
        result_name = f"cases with status '{status}'"

    if recorded_by:
        cases = cases.filter(recorded_by__username=recorded_by)
        result_name = f"cases recorded by '{recorded_by}"

    if query:
        cases = cases.filter(
            Q(case_number__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(complainant__first_name__icontains=query) |
            Q(complainant__last_name__icontains=query)
        )
        result_name = f"cases matching '{query}'"

    total_results = cases.count()
    cases = cases[:20]
    messages.info(request, f"Found {total_results} {result_name}.")
        
    
    

    total_results = cases.count()

    return render(request, 'cases/search_cases.html', {
        'cases': cases,
        'query': query,
        'status': status,
        'recorded_by': recorded_by,
        'total_results': total_results,
    })

@login_required_with_message
def witness_entry(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)

    if request.method == 'POST':
        form = WitnessForm(request.POST)
        if form.is_valid():
            witness = form.save(commit=False)
            witness.recorded_by = request.user
            witness.save()
            # Link witness to the case
            case.witnesses.add(witness)
            case.save()

            messages.success(request, "Witness statement added successfully.")

            return redirect('cases:case_details', uuid=case.uuid)
    else:
        form = WitnessForm()

    return render(request, 'cases/witness_entry.html', {'form': form, 'case': case})

@login_required_with_message
def suspect_entry(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)

    if request.method == 'POST':
        form = SuspectForm(request.POST)
        if form.is_valid():
            suspect = form.save(commit=False)
            suspect.recorded_by = request.user
            suspect.save()
            # Link suspect to the case
            case.suspects.add(suspect)
            case.save()

            messages.success(request, "Suspect added successfully.")

            return redirect('cases:case_details', uuid=case.uuid)
    else:
        form = SuspectForm()

    return render(request, 'cases/suspect_entry.html', {'form': form, 'case': case})

@login_required_with_message
def court_case_final(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)
    user = request.user
    form_title = f"Court Decision for Case #{case.case_number}"

    if user.is_authenticated and user.profile.user_role not in ['admin', 'court']:
        messages.error(request, "You do not have permission to record a court decision.")
        return redirect('cases:case_details', uuid=case.uuid)

    if case.status not in ['pending', 'open', 'in_court']:
        messages.error(request, "Court decision can only be recorded for in_court or open cases.")
        return redirect('cases:case_details', uuid=case.uuid)
    

    if request.method == 'POST':
        form = CourtDecisionForm(request.POST)
        if form.is_valid():
            # Save court decision
            decision = form.save(commit=False)
            decision.case = case
            decision.recorded_by = request.user
            decision.save()

            messages.success(request, "Court decision recorded successfully.")
            return redirect('cases:case_details', uuid=case.uuid)
    else:
        form = CourtDecisionForm()

    return render(request, 'cases/court_decision.html', {
        'form': form, 
        'case': case,
        'form_title': form_title
        })

@login_required_with_message
def suspect_page(request, case_uuid, suspect_uuid):
    case = get_object_or_404(Case, uuid=case_uuid)
    suspect = get_object_or_404(Suspect, uuid=suspect_uuid, cases=case)

    rulings = suspect.rulings.select_related("case").order_by("recorded_at")
    return render(request, "cases/suspect_page.html", {
        "case": case,
        "suspect": suspect,
        "rulings": rulings
    })

@login_required_with_message
def complainant_page(request, case_uuid, complainant_uuid):
    case = get_object_or_404(Case, uuid=case_uuid)
    complainant = get_object_or_404(Complainant, uuid=complainant_uuid)

    return render(request, "cases/complainant_page.html", {
        "case": case,
        "complainant": complainant,
    })

@login_required_with_message
def suspect_court_ruling_entry(request, uuid):
    user = request.user
    suspect = get_object_or_404(Suspect, uuid=uuid)
    form_title = f"New Court Ruling for Suspect { suspect.name }"
    case = suspect.cases.first()  # Assuming suspect is linked to at least one case

    if user.is_authenticated and user.profile.user_role not in ['admin', 'court']:
        messages.error(request, "You do not have permission to record a court decision.")
        return redirect("cases:suspect_page", case_uuid=case.uuid, suspect_uuid=suspect.uuid)


    if case.status not in ['pending', 'open', 'in_court']:
        messages.error(request, "Court ruling can only be recorded for in_court or open cases.")
        return redirect("cases:suspect_page", case_uuid=case.uuid, suspect_uuid=suspect.uuid)
    
    if request.method == "POST":
        form = SuspectCourtRulingForm(request.POST)
        if form.is_valid():
            ruling = form.save(commit=False)
            ruling.suspect = suspect
            ruling.case = case
            ruling.recorded_by = request.user
            ruling.save()

            messages.success(request, "Court ruling added successfully.")

            return redirect("cases:suspect_page", case_uuid=case.uuid, suspect_uuid=suspect.uuid)
    else:
        form = SuspectCourtRulingForm()


    return render(request, "cases/suspect_court_ruling_entry.html", {
        "case": case,
        "suspect": suspect,
        "form": form,
        "form_title": form_title
    })

@login_required_with_message
def edit_suspect_court_ruling(request, suspect_uuid, ruling_uuid):
    case = get_object_or_404(Case, suspects__uuid=suspect_uuid)
    form_title = f"Edit Court Ruling for Suspect {{ suspect.name }}"
    suspect = get_object_or_404(Suspect, uuid=suspect_uuid)
    ruling = get_object_or_404(SuspectCourtRuling, uuid=ruling_uuid, suspect=suspect)

    if request.method == "POST":
        form = SuspectCourtRulingForm(request.POST, instance=ruling)
        if form.is_valid():
            form.save()
            return redirect("cases:suspect_page", case_uuid=case.uuid, suspect_uuid=suspect.uuid)
    else:
        form = SuspectCourtRulingForm(instance=ruling)

    return render(request, "cases/suspect_court_ruling_entry.html", {
        "case": case,
        "form": form,
        "suspect": suspect,
        "ruling": ruling,
        "form_title": form_title
    })

@login_required_with_message
def witness_page(request, case_uuid, witness_uuid):
    case = get_object_or_404(Case, uuid=case_uuid)
    witness = get_object_or_404(Witness, uuid=witness_uuid)

    return render(request, "cases/witness_page.html", {
        "case": case,
        "witness": witness
    })

@login_required_with_message
def suspect_list(request):
    suspects = Suspect.objects.all().order_by("-statement_date")  # newest first
    paginator = Paginator(suspects, 10)  # 10 per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "cases/suspect_list.html", {"page_obj": page_obj})

@login_required_with_message
def witness_list(request):
    witnesses = Witness.objects.all().order_by("-date_of_statement")
    paginator = Paginator(witnesses, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "cases/witness_list.html", {
        "page_obj": page_obj})

def statistics(request):
    cases = Case.objects.all().filter(deleted=False)
    suspects = Suspect.objects.all()
    witnesses = Witness.objects.all()

    open_cases = Case.objects.filter(status="open", deleted=False)
    closed_cases = Case.objects.filter(status="closed", deleted=False)
    dismissed_cases = Case.objects.filter(status="dismissed", deleted=False)
    under_investigation = Case.objects.filter(status="under_investigation", deleted=False)
    in_court = Case.objects.all().filter(status="in_court", deleted=False)
    

    return render(request, "cases/statistics.html", {
        "number_of_cases": cases.count(),
        "number_of_suspects": suspects.count(),
        "number_of_witnesses": witnesses.count(),
        "number_of_open_cases": open_cases.count(),
        "number_of_closed_cases": closed_cases.count(),
        "number_of_dismissed_cases": dismissed_cases.count(),
        "number_of_under_investigation": under_investigation.count(),
        "number_of_in_court": in_court.count()
    })

def case_pdf_view(request, uuid):
    from datetime import datetime
    case = get_object_or_404(Case, uuid=uuid)
    html_content = render_to_string('cases/case_pdf.html', {'case': case})
    pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response['Content-Disposition'] = f'filename=case_report_{case.case_number}_{timestamp}.pdf'
    return response

def reports(request):
    search_query = request.GET.get('q', '')
    if request.user.profile.user_role == 'admin':
        cases = Case.objects.all().filter().order_by('-created_at')
    else:
        cases = Case.objects.all().filter(deleted=False).order_by('-created_at')

    # Search by case number, title, or complainant name
    if search_query:
        cases = cases.filter(
            case_number__icontains=search_query
        ) | cases.filter(
            title__icontains=search_query
        ) | cases.filter(
            complainant__first_name__icontains=search_query
        ) | cases.filter(
            complainant__last_name__icontains=search_query
        )

    paginator = Paginator(cases, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cases': page_obj,
        'search_query': search_query,
    }
    return render(request, 'cases/reports.html', context)

def delete_case(request, case_uuid):
    case = get_object_or_404(Case, uuid=case_uuid)
    case.deleted = True
    case.deleted_at = timezone.now()
    case.deleted_by = request.user
    case.save()

    messages.success(request, f"Case {case.case_number} deleted successfully.")
    return redirect("cases:view_cases")

def court_rulings_list(request):
    decisions = CourtDecision.objects.select_related("case", "recorded_by").all()

    # Search query
    query = request.GET.get("q")
    if query:
        decisions = decisions.filter(
            Q(case__case_number__icontains=query)
            | Q(decision_text__icontains=query)
            | Q(decision_type__icontains=query)
            | Q(recorded_by__username__icontains=query)
        )

    # Filter by decision type
    filter_type = request.GET.get("type")
    if filter_type:
        decisions = decisions.filter(decision_type=filter_type)

    # Filter by date range
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            decisions = decisions.filter(decision_date__gte=start_date_obj)
        except ValueError:
            pass  # ignore invalid date

    if end_date:
        try:
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
            decisions = decisions.filter(decision_date__lt=end_date_obj)
        except ValueError:
            pass

    # Pagination
    paginator = Paginator(decisions, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query or "",
        "filter_type": filter_type or "",
        "start_date": start_date or "",
        "end_date": end_date or "",
    }
    return render(request, "cases/court_rulings_list.html", context)


def court_ruling_detail(request, uuid):
    decision = get_object_or_404(CourtDecision, uuid=uuid)

    context = {
        "decision": decision
    }
    return render(request, "cases/court_ruling_detail.html", context)