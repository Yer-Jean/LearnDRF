from django.core.management import BaseCommand

from courses.models import Payment


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        payment_list = [
            {
                "student": "Luke Skywalker",
                "payment_date": "2023-07-18",
                "course": 1,
                "amount": 99,
                "payment_type": "card"
            },
            {
                "student": "Han Solo",
                "payment_date": "2023-07-25",
                "course": 1,
                "amount": 99,
                "payment_type": "cash"
            },
            {
                "student": "Yoda",
                "payment_date": "2023-09-25",
                "lesson": 1,
                "amount": 19,
                "payment_type": "card"
            },
            {
                "student": "Yoda",
                "payment_date": "2023-10-25",
                "lesson": 2,
                "amount": 39,
                "payment_type": "card"
            },
            {
                "student": "Yoda",
                "payment_date": "2023-11-25",
                "lesson": 3,
                "amount": 29,
                "payment_type": "card"
            },
            {
                "student": "Princess Leia",
                "payment_date": "2023-07-18",
                "lesson": 3,
                "amount": 29,
                "payment_type": "cash"
            },
            {
                "student": "Darth Vader",
                "payment_date": "2023-11-30",
                "lesson": 3,
                "amount": 29,
                "payment_type": "card"
            },
            {
                "student": "Obi-Wan Kenobi",
                "payment_date": "2023-07-18",
                "course": 2,
                "amount": 299,
                "payment_type": "cash"
            },
            {
                "student": "Chewbacca",
                "payment_date": "2023-10-25",
                "lesson": 1,
                "amount": 19,
                "payment_type": "cash"
            },
            {
                "student": "Chewbacca",
                "payment_date": "2023-10-25",
                "course": 2,
                "amount": 129,
                "payment_type": "cash"
            }
        ]

        payments_for_create = []
        for payment_item in payment_list:
            payments_for_create.append(Payment(**payment_item))

        Payment.objects.bulk_create(payments_for_create)
