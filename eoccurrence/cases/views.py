from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import CharField, Value

from .forms import ComplainantForm, CaseForm, WitnessForm,  SuspectForm
from .models import Complainant, Case

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
    cases = Case.objects.none()
    total_results = 0

    if query:
        # Annotate recorded_by full name
        qs = Case.objects.annotate(
            recorded_by_full_name=Concat(
                'recorded_by__first_name',
                Value(' '),
                'recorded_by__last_name',
                output_field=CharField()
            )
        ).filter(
            Q(case_number__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(complainant__first_name__icontains=query) |
            Q(complainant__last_name__icontains=query) |
            Q(recorded_by_full_name__icontains=query)   # search full name only
        )

        total_results = qs.count()  # full count
        cases = qs[:20]             # limit results shown

        messages.info(request, f"Found {total_results} cases matching '{query}'.")

    return render(request, 'cases/search_cases.html', {
        'cases': cases,
        'query': query,
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