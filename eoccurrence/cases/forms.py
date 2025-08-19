from django import forms
from .models import Complainant, Case, Suspect, Witness, CourtDecision, SuspectCourtRuling

INPUT_CLASSES = 'w-full py-2 px-4 rounded-xl bg-white border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'

class ComplainantForm(forms.ModelForm):
    class Meta:
        model = Complainant
        fields = ['first_name', 'last_name', 'id_number','phone_number', 'email', 'gender', 'date_of_birth',  'address', 'county', 'sub_county']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name', 
                'class': INPUT_CLASSES
            }),
            'last_name': forms.TextInput(attrs=
                {'placeholder': 'Last Name', 
                'class': INPUT_CLASSES
            }),
            'id_number': forms.TextInput(attrs={
                'placeholder': 'ID Number', 
                'class': INPUT_CLASSES
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Phone Number', 
                'class': INPUT_CLASSES
            }),
            
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email', 
                'class': INPUT_CLASSES
            }),
            'gender': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date', 'class': INPUT_CLASSES
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Address', 
                'rows': '4',
                'cols': '40',
                'style': 'resize: none',
                'class': INPUT_CLASSES
            }),
            'county': forms.TextInput(attrs={
                'placeholder': 'County', 
                'class': INPUT_CLASSES
            }),
            'sub_county': forms.TextInput(attrs={
                'placeholder': 'Sub County', 
                'class': INPUT_CLASSES
            }),
        }

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = ['case_number', 'recorded_by', 'date_reported', 'complainant', 'suspects', 'witnesses']
        fields = ['case_type', 'title', 'location', 'description', 'status', 'incident_date', 'court_date']
        widgets = {
            'case_type': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Case Title', 
                'class': INPUT_CLASSES
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Incident Location', 
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES, 
                'placeholder': 'Case Description',
                'rows': '4',
                'cols': '40',
                'style': 'resize: none',
            }),
            'status': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'incident_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': INPUT_CLASSES,
            }),
            'court_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': INPUT_CLASSES,
            }),
        }

class SuspectForm(forms.ModelForm):
    class Meta:
        model = Suspect
        fields = ['name', 'national_id', 'contact_info', 'date_of_birth', 'address', 'statement', 'arrest_date', 'arrest_location', 'charges']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Suspect Name', 
                'class': INPUT_CLASSES
            }),
            'national_id': forms.TextInput(attrs={
                'placeholder': 'National ID', 
                'class': INPUT_CLASSES
            }),
            'contact_info': forms.TextInput(attrs={
                'placeholder': 'Contact Information', 
                'class': INPUT_CLASSES
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date', 
                'class': INPUT_CLASSES
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Address', 
                'rows': '4',
                'cols': '40',
                'style': 'resize: none',
                'class': INPUT_CLASSES
            }),
            'statement': forms.Textarea(attrs={
                'placeholder': 'Statement', 
                'rows': '4',
                'cols': '40',
                'style': 'resize: none',
                'class': INPUT_CLASSES
            }),
            'arrest_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': INPUT_CLASSES
            }),
            'arrest_location': forms.TextInput(attrs={
                'placeholder': 'Arrest Location', 
                'class': INPUT_CLASSES
            }),
            'charges': forms.Textarea(attrs={
                'placeholder': 'Charges', 
                'rows': '4',
                'cols': '40',               
                'style': 'resize: none',
                'class': INPUT_CLASSES
            }),
        }

        def clean(self):
            cleaned_data = super().clean()
            # Check if all fields are empty
            if not any(cleaned_data.get(f) for f in self.Meta.fields):
                raise forms.ValidationError(
                    "You must fill in at least one field before submitting."
                )
            return cleaned_data

class WitnessForm(forms.ModelForm):
    class Meta:
        model = Witness
        fields = ['name', 'national_id', 'contact_info', 'date_of_birth', 'address', 'statement']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Witness Name', 
                'class': INPUT_CLASSES
            }),
            'national_id': forms.TextInput(attrs={
                'placeholder': 'National ID', 
                'class': INPUT_CLASSES
            }),
            'contact_info': forms.TextInput(attrs={
                'placeholder': 'Contact Information', 
                'class': INPUT_CLASSES
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date', 
                'class': INPUT_CLASSES
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Address', 
                'rows': '4',
                'cols': '40',
                'style': 'resize: none',
                'class': INPUT_CLASSES
            }),
            'statement': forms.Textarea(attrs={
                'placeholder': 'Witness Statement', 
                'rows': '4',
                'cols': '40',
                'style': 'resize: none',
                'class': INPUT_CLASSES
            }),
        }

        def clean(self):
            cleaned_data = super().clean()
            # Check if all fields are empty
            if not any(cleaned_data.get(f) for f in self.Meta.fields):
                raise forms.ValidationError(
                    "You must fill in at least one field before submitting."
                )
            return cleaned_data
        
class CourtDecisionForm(forms.ModelForm):
    class Meta:
        model = CourtDecision
        fields = ['decision_type', 'decision_text']
        widgets = {
            'decision_type': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'decision_text': forms.Textarea(attrs={
                'placeholder': 'Decision Details', 
                'rows': '4',
                'cols': '40',
                'style': 'resize: none',
                'class': INPUT_CLASSES
            }),
        }

class SuspectCourtRulingForm(forms.ModelForm):
    class Meta:
        model = SuspectCourtRuling
        fields = ["ruling_type", "ruling_text"]

        widgets = {
            "ruling_type": forms.Select(attrs={
                "class": "w-full p-2 border rounded-lg"
            }),
            "ruling_text": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded-lg",
                "rows": 3,
                "placeholder": "Enter details of the ruling..."
            }),
        }