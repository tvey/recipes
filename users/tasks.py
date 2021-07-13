from django.conf import settings
from django.core.mail import send_mail

from config.celery import app


@app.task
def send_email(user_email, subject=None, message=None, html_message=None):
    """General task for sending email."""
    send_mail(
        subject if subject else '',
        message if message else '',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
        html_message=html_message,
    )
