from django.core.mail import send_mail
import random
from django.conf import settings
from apps.users.models import User
from udemy.celery import app


@app.task()
def send_otp_email(email):
    otp = _generate_otp()
    _send_email(email, otp)
    _update_user_otp(email, otp)


def _generate_otp():
    return random.randint(1000, 9999)


def _send_email(email, otp):
    subject = "Your account verification email"
    message = f"Your otp is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])


def _update_user_otp(email, otp):
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
