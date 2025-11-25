from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Userprofile

INPUT_CLASSES = 'w-full py-2 px-4 rounded-xl bg-white border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
class loginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username or ID number',
        'class': INPUT_CLASSES,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password-input',
        'placeholder': 'Your password',
        'class': INPUT_CLASSES,
    }))
    error_messages = {
        'invalid_login': _("Invalid username or ID number, or password."),
    }

    def confirm_login_allowed(self, user):
        # If your UserProfile is linked via OneToOne
        if hasattr(user, "profile"):
            if not user.profile.is_active:
                raise ValidationError(
                    "Your account is inactive. Please contact the admin.",
                    code="inactive",
                )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    id_number = forms.CharField(required=True, max_length=20)
    phone_number = forms.CharField(required=True, max_length=10)
    address = forms.CharField(widget=forms.Textarea, required=True)
    user_role = forms.ChoiceField(choices=Userprofile.USER_ROLES, required=True)
    department = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    profile_picture = forms.ImageField(required=False)

    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': INPUT_CLASSES,
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'First name',
        'class': INPUT_CLASSES,
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Last name',
        'class': INPUT_CLASSES,
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'id_number', 'phone_number', 'address', 'user_role', 'department', 'date_of_birth']

        help_texts = {
        'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        'first_name': 'Required. Your first name.',
        'last_name': 'Required. Your last name.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': INPUT_CLASSES,
            'id': 'password1'
        })

        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repeat Password',
            'class': INPUT_CLASSES,
            'id': 'password2'
        })

        self.fields['id_number'].widget.attrs.update({
            'placeholder': 'ID number',
            'class': INPUT_CLASSES
        })

        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Phone number',
            'class': INPUT_CLASSES
        }),

        self.fields['email'].widget.attrs.update({
            'placeholder': 'example@example.com',
            'class': INPUT_CLASSES
        })

        self.fields['address'].widget.attrs.update({
            'placeholder': 'Address',
            'rows': '4',
            'cols': '40',
            'style': 'resize: none',
            'class': INPUT_CLASSES
        })
        self.fields['user_role'].widget.attrs.update({
            'class': INPUT_CLASSES
        })
        self.fields['department'].widget.attrs.update({
            'placeholder': 'Department',
            'class': INPUT_CLASSES
        })
        self.fields['date_of_birth'].widget.attrs.update({
            'placeholder': 'DD/MM/YYYY',
            'class': INPUT_CLASSES,
            'type': 'date'
        })

        self.fields['id_number'].help_text = 'Required. Your Police, Court or National ID number.'
        self.fields['phone_number'].help_text = 'Required. Your phone number.'
        self.fields['email'].help_text = 'Required. Enter your student email.'
        self.fields['address'].help_text = 'Required. Your address.'
        self.fields['user_role'].help_text = 'This field is automatically set to Student and only admins can change.'
        self.fields['department'].help_text = 'Required. Your department.'
        self.fields['date_of_birth'].help_text = 'Required. Your date of birth.'


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            Userprofile.objects.create(
                user=user,
                id_number=self.cleaned_data.get('id_number'),
                user_role=self.cleaned_data.get('user_role'),
                phone_number=self.cleaned_data.get('phone_number'),
                address=self.cleaned_data.get('address'),
                department=self.cleaned_data.get('department'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
            )
        return user
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES}),
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
        }

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['id_number', 'phone_number', 'address', 'user_role', 'department', 'date_of_birth']
        widgets = {
            'id_number': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'phone_number': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'address': forms.Textarea(attrs={'rows': '4', 'cols': '40', 'style': 'resize: none', 'class': INPUT_CLASSES}),
            'user_role': forms.Select(attrs={'class': INPUT_CLASSES}),
            'department': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
        }