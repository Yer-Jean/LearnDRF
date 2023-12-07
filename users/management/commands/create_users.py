from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create a superuser with the specified email'

    def handle(self, *args, **options):
        users_list = [
            {
                "email": "yerg@mail.ru",
                "password": "123qwe456rty"
            },            {
                "email": "Chewbacca@mail.com",
                "password": "Chewbacca"
            },            {
                "email": "OWKenobi@mail.com",
                "password": "OWKenobi"
            },            {
                "email": "DVader@mail.com",
                "password": "DVader"
            },            {
                "email": "Leia@mail.com",
                "password": "Leia"
            },            {
                "email": "Yoda@mail.com",
                "password": "Yoda"
            },
            {
                "email": "HanSolo@mail.com",
                "password": "HanSolo"
            },
            {
                "email": "Skywalker@mail.com",
                "password": "Skywalker"
            },
        ]

        for user in users_list:
            user_for_create = User.objects.create(
                email=user['email'],
                # is_superuser=True,
                # is_staff=True,
                is_active=True
            )
            user_for_create.set_password(user['password'])
            user_for_create.save()
