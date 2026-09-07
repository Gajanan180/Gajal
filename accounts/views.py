from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    LoginForm,
    OTPVerifyForm,
    PasswordResetConfirmForm,
    PasswordResetRequestForm,
    RegisterForm,
)
from .models import EmailOTP, User
from .utils import send_otp_email


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.is_active = True
            user.save()
            otp_obj = EmailOTP.create_otp(user.email, EmailOTP.Purpose.SIGNUP)
            send_otp_email(user.email, otp_obj.otp, EmailOTP.Purpose.SIGNUP)
            request.session['pending_verify_email'] = user.email
            messages.success(request, 'Account created! Check your email/console for OTP.')
            return redirect('accounts:verify_otp')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_otp_view(request):
    email = request.session.get('pending_verify_email')
    if not email:
        messages.error(request, 'No pending verification. Please register first.')
        return redirect('accounts:register')

    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            otp_obj = EmailOTP.objects.filter(
                email=email,
                purpose=EmailOTP.Purpose.SIGNUP,
                otp=form.cleaned_data['otp'],
            ).first()
            if otp_obj and otp_obj.is_valid():
                otp_obj.is_used = True
                otp_obj.save()
                user = User.objects.get(email=email)
                user.is_verified = True
                user.save()
                del request.session['pending_verify_email']
                messages.success(request, 'Email verified! You can now log in.')
                return redirect('accounts:login')
            messages.error(request, 'Invalid or expired OTP.')
    else:
        form = OTPVerifyForm()

    return render(request, 'accounts/verify_otp.html', {'form': form, 'email': email})


def resend_otp_view(request):
    email = request.session.get('pending_verify_email')
    if not email:
        return redirect('accounts:register')
    otp_obj = EmailOTP.create_otp(email, EmailOTP.Purpose.SIGNUP)
    send_otp_email(email, otp_obj.otp, EmailOTP.Purpose.SIGNUP)
    messages.success(request, 'A new OTP has been sent.')
    return redirect('accounts:verify_otp')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_verified and not user.is_superuser:
                messages.error(request, 'Please verify your email before logging in.')
                request.session['pending_verify_email'] = user.email
                return redirect('accounts:verify_otp')
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            if user.is_merchant:
                return redirect('merchants:dashboard')
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                otp_obj = EmailOTP.create_otp(email, EmailOTP.Purpose.PASSWORD_RESET)
                send_otp_email(email, otp_obj.otp, EmailOTP.Purpose.PASSWORD_RESET)
            request.session['reset_email'] = email
            messages.success(request, 'If the email exists, an OTP has been sent.')
            return redirect('accounts:password_reset_confirm')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset.html', {'form': form})


def password_reset_confirm_view(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('accounts:password_reset')

    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            otp_obj = EmailOTP.objects.filter(
                email=email,
                purpose=EmailOTP.Purpose.PASSWORD_RESET,
                otp=form.cleaned_data['otp'],
            ).first()
            if otp_obj and otp_obj.is_valid():
                otp_obj.is_used = True
                otp_obj.save()
                user = User.objects.get(email=email)
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                del request.session['reset_email']
                messages.success(request, 'Password reset successful. Please log in.')
                return redirect('accounts:login')
            messages.error(request, 'Invalid or expired OTP.')
    else:
        form = PasswordResetConfirmForm()

    return render(request, 'accounts/password_reset_confirm.html', {'form': form, 'email': email})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
