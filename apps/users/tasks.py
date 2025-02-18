import os

from celery import shared_task
from django.core.mail import send_mail

FROM_EMAIL = os.getenv('EMAIL_HOST_USER')


@shared_task
def send_verification_email(email, code):
    subject = "Your Verification Code"
    message = f"Your verification code is: {code}"
    from_email = FROM_EMAIL  # Change this
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_verification_phone(phone, code):
    message = f"your verification code is: {code}"
    print(f"SMS: {message}")