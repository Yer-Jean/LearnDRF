from django.core.management import BaseCommand

from courses.models import Payment


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        payment_list = [
            {
                "student_id": 8,
                "payment_date": "2023-07-18",
                "course_id": 1,
                "amount": 99,
                "payment_type": "bank"
            },
            {
                "student_id": 7,
                "payment_date": "2023-07-25",
                "course_id": 1,
                "amount": 99,
                "payment_type": "cash"
            },
            {
                "student_id": 6,
                "payment_date": "2023-09-25",
                "lesson_id": 1,
                "amount": 19,
                "payment_type": "bank"
            },
            {
                "student_id": 6,
                "payment_date": "2023-10-25",
                "lesson_id": 2,
                "amount": 39,
                "payment_type": "bank"
            },
            {
                "student_id": 6,
                "payment_date": "2023-11-25",
                "lesson_id": 3,
                "amount": 29,
                "payment_type": "bank"
            },
            {
                "student_id": 5,
                "payment_date": "2023-07-18",
                "lesson_id": 3,
                "amount": 29,
                "payment_type": "cash"
            },
            {
                "student_id": 4,
                "payment_date": "2023-11-30",
                "lesson_id": 3,
                "amount": 29,
                "payment_type": "bank"
            },
            {
                "student_id": 3,
                "payment_date": "2023-07-18",
                "course_id": 2,
                "amount": 299,
                "payment_type": "cash"
            },
            {
                "student_id": 2,
                "payment_date": "2023-10-25",
                "lesson_id": 1,
                "amount": 19,
                "payment_type": "cash"
            },
            {
                "student_id": 2,
                "payment_date": "2023-10-25",
                "course_id": 2,
                "amount": 129,
                "payment_type": "cash"
            }
        ]

        payments_for_create = []
        for payment_item in payment_list:
            payments_for_create.append(Payment(**payment_item))

        Payment.objects.bulk_create(payments_for_create)
