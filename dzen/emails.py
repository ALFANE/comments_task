from django.conf import settings
from django.core.mail import send_mail


def send_email(recipient_list=None, activate_url=None):
    subject = "Thank you for comment"
    message = "You have successfully left a comment."
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list)
