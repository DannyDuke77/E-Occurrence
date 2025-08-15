from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q

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
        'form': form,
        'complainant': complainant
    })

def view_cases(request):
    cases = Case.objects.all()

    return render(request, 'cases/view_cases.html', {
        'cases': cases
        })

@login_required
def case_details(request, uuid):
    case = get_object_or_404(Case, uuid=uuid)

    wittnesses = case.witnesses.all()
    suspects = case.suspects.all()

    return render(request, 'cases/case_details.html', {
        'case': case,
        'witnesses': wittnesses,
        'suspects': suspects
        })

def search_cases(request):
    query = request.GET.get('query', '')
    cases = Case.objects.none()

    if query:
        # Search by case number, title, description, location, or complainant's name
        cases = Case.objects.filter(Q(case_number__icontains=query) | Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query) | Q(complainant__first_name__icontains=query) | Q(complainant__last_name__icontains=query))

        messages.info(request, f"Found {cases.count()} cases matching '{query}'.")

    return render(request, 'cases/search_cases.html', {
        'cases': cases,
        'query': query
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