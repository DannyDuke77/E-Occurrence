from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import CharField, Value
from django.core.paginator import Paginator

from .forms import ComplainantForm, CaseForm, WitnessForm,  SuspectForm, CourtDecisionForm, SuspectCourtRulingForm
from .models import Complainant, Case, Suspect, Witness, CourtDecision, SuspectCourtRuling

from accounts.models import Userprofile

from .forms import CaseForm

@login_required
def complainant_entry(request):
    if request.method == 'POST':
        form = ComplainantForm(request.POST)
        if form.is_valid():
            complainant = form.save()
            return redirect('cases:case_entry', uuid=complainant.uuid)
    else:
        form = ComplainantForm()

    return render(request, 'cases/complainant_entry.html', {'form': form})


@login_required
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
            return redirect("/")  # or any success page
    else:
        form = CaseForm()

    return render(request, 'cases/case_entry.html', {
        'form_title': form_title,
        'form': form,
        'complainant': complainant
    })

def view_cases(request):
    # Get all cases
    # qs stands for QuerySet
    qs = Case.objects.all()
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

def edit_case(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)
    form_title = f"Edit Case #{ case.case_number }"
    complainant = case.complainant

    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
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

def case_details(request, uuid):
    if request.user.is_authenticated:
        case = get_object_or_404(Case, uuid=uuid)
        witnesses = case.witnesses.all()
        suspects = case.suspects.all()
        
        return render(request, "cases/case_details.html", {
            "case": case,
            "witnesses": witnesses,
            "suspects": suspects,
        })
    else:
        messages.error(request, "You need to be logged in to view case details.")
        return redirect('accounts:login')
    
def search_cases(request):
    query = request.GET.get('query', '').strip()
    status = request.GET.get('status', '')
    recorded_by = request.GET.get('recorded_by', '')

    cases = Case.objects.all()

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

@login_required
def witness_entry(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)

    if request.method == 'POST':
        form = WitnessForm(request.POST)
        if form.is_valid():
            witness = form.save()
            # Link witness to the case
            case.witnesses.add(witness)
            case.save()

            messages.success(request, "Witness statement added successfully.")

            return redirect('cases:case_details', uuid=case.uuid)
    else:
        form = WitnessForm()

    return render(request, 'cases/witness_entry.html', {'form': form, 'case': case})

@login_required
def suspect_entry(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)

    if request.method == 'POST':
        form = SuspectForm(request.POST)
        if form.is_valid():
            suspect = form.save()
            # Link suspect to the case
            case.suspects.add(suspect)
            case.save()

            messages.success(request, "Suspect added successfully.")

            return redirect('cases:case_details', uuid=case.uuid)
    else:
        form = SuspectForm()

    return render(request, 'cases/suspect_entry.html', {'form': form, 'case': case})

def court_case_final(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)
    form_title = f"Court Decision for Case #{case.case_number}"

    if case.status not in ['pending', 'open', 'in_court']:
        messages.error(request, "Court decision can only be recorded for pending or open cases.")
        return redirect('cases:case_details', uuid=case.uuid)
    

    if request.method == 'POST':
        form = CourtDecisionForm(request.POST)
        if form.is_valid():
            # Save court decision
            decision = form.save(commit=False)
            decision.case = case
            decision.recorded_by = request.user
            decision.save()

            if decision.decision_type == 'BAIL_GRANTED':
                case.bail_decision = 'granted'
                case.status = 'in_court'
                case.save()
            
            if decision.decision_type == 'DISMISSED':
                case.bail_decision = 'not_applicable'
                case.status = 'dismissed'
                case.save()
            
            if decision.decision_type == 'SENTENCED':
                case.bail_decision = 'not_applicable'
                case.status = 'closed'
                case.save()

            messages.success(request, "Court decision recorded successfully.")
            return redirect('cases:case_details', uuid=case.uuid)
    else:
        form = CourtDecisionForm()

    return render(request, 'cases/court_decision.html', {
        'form': form, 
        'case': case,
        'form_title': form_title
        })

def court_suspect_ruling(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)
    form_title = f"Suspect Ruling for Case #{case.case_number}"

    if request.method == 'POST':
        form = CourtDecisionForm(request.POST)
        if form.is_valid():
            ruling = form.save(commit=False)
            ruling.case = case
            ruling.recorded_by = request.user
            ruling.save()

            messages.success(request, "Court ruling recorded successfully.")
            return redirect('cases:case_details', uuid=case.uuid)
    else:
        form = CourtDecisionForm()

    return render(request, 'cases/court_ruling.html', {
        'form': form, 
        'case': case,
        'form_title': form_title
    })

@login_required
def suspect_page(request, case_uuid, suspect_uuid):
    case = get_object_or_404(Case, uuid=case_uuid)
    suspect = get_object_or_404(Suspect, uuid=suspect_uuid, cases=case)

    rulings = suspect.rulings.select_related("case").order_by("-recorded_at")
    return render(request, "cases/suspect_page.html", {
        "case": case,
        "suspect": suspect,
        "rulings": rulings
    })


@login_required
def suspect_court_ruling_entry(request, uuid):
    suspect = get_object_or_404(Suspect, uuid=uuid)
    form_title = f"New Court Ruling for Suspect { suspect.name }"
    case = suspect.cases.first()  # Assuming suspect is linked to at least one case

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

def witness_page(request, case_uuid, witness_uuid):
    case = get_object_or_404(Case, uuid=case_uuid)
    witness = get_object_or_404(Witness, uuid=witness_uuid)

    return render(request, "cases/witness_page.html", {
        "case": case,
        "witness": witness
    })

def suspect_list(request):
    suspects = Suspect.objects.all().order_by("-statement_date")  # newest first
    paginator = Paginator(suspects, 10)  # 10 per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "cases/suspect_list.html", {"page_obj": page_obj})


def witness_list(request):
    witnesses = Witness.objects.all().order_by("-date_of_statement")
    paginator = Paginator(witnesses, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "cases/witness_list.html", {
        "page_obj": page_obj})

def statistics(request):
    cases = Case.objects.all()
    suspects = Suspect.objects.all()
    witnesses = Witness.objects.all()

    open_cases = Case.objects.filter(status="open")
    closed_cases = Case.objects.filter(status="closed")
    dismissed_cases = Case.objects.filter(status="dismissed")
    under_investigation = Case.objects.filter(status="under_investigation")
    in_court = Case.objects.all().filter(status="in_court")
    

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