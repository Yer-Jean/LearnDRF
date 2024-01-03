from datetime import timedelta

from django.utils import timezone
from celery import shared_task

from users.models import User

DAYS_THRESHOLD = 30


@shared_task
def disabling_users():
    today = timezone.now().date()
    active_users = User.objects.filter(is_active=True)
    for user in active_users:
        if user.last_login and (today - user.last_login.date()) > timedelta(days=DAYS_THRESHOLD):
            user.is_active = False
            user.save()
