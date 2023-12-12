from django.conf import settings
from django.core.mail import send_mail


def send_course_update_notification(subscribers, message):
    send_mail(
                subject='Updates on course',
                message=message,
                # message=f'The course "{course.title}" has been updated or new lessons have been released',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=subscribers,
                fail_silently=False,
            )
