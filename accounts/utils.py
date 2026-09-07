from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_otp_email(email, otp, purpose):
    subject_map = {
        'signup': 'Verify your Gajal Food account',
        'password_reset': 'Reset your Gajal Food password',
    }
    subject = subject_map.get(purpose, 'Gajal Food OTP')
    message = render_to_string('accounts/emails/otp_email.txt', {
        'otp': otp,
        'purpose': purpose.replace('_', ' '),
    })
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
