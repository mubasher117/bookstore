from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_purchase_confirmation(user_email, order_details):
    subject = "Your Book Order Confirmation"
    message = f"Hi {user_email},\n\nThis email confirms your recent purchase on our bookstore.\n\nOrder details:\n{order_details}\n\nThank you for your business!\n\nSincerely,\nThe Bookstore Team"
    send_mail(subject, message, None, [user_email])