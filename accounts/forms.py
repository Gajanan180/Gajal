from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    role = forms.ChoiceField(
        choices=[
            (User.Role.CUSTOMER, 'Customer - Order food'),
            (User.Role.MERCHANT, 'Merchant - Sell food'),
        ],
        widget=forms.RadioSelect,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'role', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )


class OTPVerifyForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit OTP'}),
    )


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Registered email'}),
    )


class PasswordResetConfirmForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('new_password1') != cleaned.get('new_password2'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned
