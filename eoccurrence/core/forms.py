from django import forms
from .models import SupportRequest

INPUT_CLASSES = 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 text-sm'

class SupportRequestForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name (Optional)',
                'class': INPUT_CLASSES
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email (Optional)',
                'class': INPUT_CLASSES
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Enter your message. Maximum 1000 characters (Required)',
                'class': INPUT_CLASSES,
                'rows': 6,
                'maxlength': 1000,
                'style': 'resize: none'
            }),
        }
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("This field is required.")
        if len(message) > 1000:
            raise forms.ValidationError("Message cannot exceed 1000 characters.")
        
        return message