from django.core.mail import send_mail
from django.conf import settings
from udemy.celery import app


@app.task()
def send_order_completion_email(email):
    _send_email(email)


def _send_email(email):
    subject = "Order complete! Start learning now."
    message = "Your order’s been processed"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
