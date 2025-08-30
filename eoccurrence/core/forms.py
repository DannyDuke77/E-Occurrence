from django import forms
from .models import SupportRequest

class SupportRequestForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name (Optional)',
                'class': 'w-full rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 px-4 py-3 shadow-sm'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email (Optional)',
                'class': 'w-full rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 px-4 py-3 shadow-sm'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Enter your message. Maximum 1000 characters (Required)',
                'class': 'w-full rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 px-4 py-3 shadow-sm resize-none',
                'rows': 6,
                'maxlength': 1000
            }),
        }
