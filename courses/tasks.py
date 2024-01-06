from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from courses.models import Subscription


# @shared_task
# def send_course_update_notification(subscribers, message):
#     send_mail(
#                 subject='Updates on course',
#                 message=message,
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=subscribers,
#                 fail_silently=False,
#             )

# Этот вариант подсказан наставником: нужно ставить как можно меньше параметров, желательно
# скаляры. Фильтр по подписанным пользователям будет работать в асинхронном режиме
@shared_task
def send_course_update_notification(pk, message):
    subscribers = list(Subscription.objects.filter(course=pk).values_list('user__email', flat=True))

    send_mail(
                subject='Updates on course',
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=subscribers,
                fail_silently=False,
            )
