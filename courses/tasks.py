from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_course_update_notification(subscribers, message):
    send_mail(
                subject='Updates on course',
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=subscribers,
                fail_silently=False,
            )
