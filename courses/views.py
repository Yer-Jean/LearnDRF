import requests
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from django.conf import settings
from courses.paginators import CourseAndLessonPaginator
from courses.permissions import IsNotModerator, IsOwner
from courses.serializers import *
from courses.services import send_course_update_notification
from users.models import User


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseAndLessonPaginator

    def get_permissions(self):

        match self.action:
            case 'create':
                permission_classes = [IsAuthenticated, IsNotModerator]
            case 'destroy':
                permission_classes = [IsAuthenticated, IsNotModerator, IsOwner]
            case 'retrieve' | 'update' | 'partial_update':
                permission_classes = [IsAuthenticated, IsOwner]
            case 'list':
                permission_classes = [IsAuthenticated, IsOwner | ~IsNotModerator]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def perform_update(self, serializer):
        instance = serializer.save()

        # Получаем всех подписчиков курса
        subscribers = Subscription.objects.filter(course=instance).values_list('user__email', flat=True)
        # Отправляем письмо
        send_course_update_notification(subscribers,
                                        f'The course "{instance.title}" has been updated')

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def get_queryset(self):
    #     if self.action == 'list':
    #         return Course.objects.filter(owner=self.request.user)
    #     return super().get_queryset()

    def get(self, request):
        if self.action == 'list':
            queryset = Course.objects.filter(owner=self.request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()
        # Получаем всех подписчиков курса
        subscribers = Subscription.objects.filter(course=lesson.course).values_list('user__email', flat=True)
        # Отправляем письмо
        send_course_update_notification(subscribers,
                                        f'New lesson have been released on course "{lesson.course}"')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsNotModerator]
    pagination_class = CourseAndLessonPaginator

    # def get_queryset(self):
    #     if self.request.user.groups.name != 'moderators':
    #         return Lesson.objects.filter(owner=self.request.user)
    #     return super().get_queryset()

    def get(self, request):
        if self.request.user.groups.name != 'moderators':
            queryset = Lesson.objects.filter(owner=self.request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        instance = serializer.save()
        # Получаем всех подписчиков курса
        subscribers = Subscription.objects.filter(course=instance.course).values_list('user__email', flat=True)
        # Отправляем письмо
        send_course_update_notification(subscribers, f'Lesson "{instance.title}"'
                                        f' has been updated on course "{instance.course}"')
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator, IsOwner]


class PaymentByCardCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.student = self.request.user

        session_id = self.create_stripe_payment(payment)
        payment.payment_reference = session_id

        payment.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_stripe_payment(self, payment):
        """ Метод создает платеж, с поледовательным созданием продукта,
        цены на него и сессии для платежа по кредитной карте"""
        # Создаем продукт с наименованием из созданного платежа
        url = settings.STRIPE_API_URL + 'products'
        data = {
            'name': payment.course if payment.course else payment.lesson,
        }
        response = requests.post(url, auth=(settings.STRIPE_SECRET_KEY, ''), data=data)

        # Создаем цену на созданный продукт
        url = settings.STRIPE_API_URL + 'prices'
        data = {
            'currency': 'usd',
            'unit_amount': payment.amount,
            'recurring[interval]': None,
            'product_data[name]': payment.course if payment.course else payment.lesson,
        }
        response = requests.post(url, auth=(settings.STRIPE_SECRET_KEY, ''), data=data)

        price_id = response.json().get('id')

        # Создаем сессию на сервисе stripe.com
        url = settings.STRIPE_API_URL + 'checkout/sessions'
        success_url = 'https://example.com/success'
        quantity = 1
        data = {
            'success_url': success_url,
            'line_items[0][price]': price_id,
            'line_items[0][quantity]': quantity,
            'mode': 'payment',
        }
        response = requests.post(url, auth=(settings.STRIPE_SECRET_KEY, ''), data=data)
        # print(response.json())
        return response.json().get('id')


class PaymentByCardGetAPIView(APIView):

    def get(self, request):
        """ Метод возвращает платежи, которые были оплачены """
        paid_payments = []

        # Запрашиваем все платежные сессии со stripe.com
        url = settings.STRIPE_API_URL + 'checkout/sessions'
        response = requests.get(url, auth=(settings.STRIPE_SECRET_KEY, ''))
        payments = response.json()['data']
        # Если сессия оплачена, то меняем статус is_paid в модели Payments
        for payment in payments:
            if payment['payment_status'] in ['paid', 'completed']:
                pay = Payment.objects.get(payment_reference=payment['id'])
                # Если ранее эта сессия была не оплачена, то меняем статус на is_paid=True
                if not pay.is_paid:
                    pay.is_paid = True
                    pay.save()
                    # Собираем свежеоплаченные сессии используя сериалайзер для последующего вывода
                    serialized_data = PaymentHistorySerializer(pay).data
                    paid_payments.append(serialized_data)
        # Возвращаем для вывода те платежи, которые были оплачены с последнего запуска этого метода
        return Response(paid_payments)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_type',)
    ordering_fields = ('payment_date',)


class StudentPaymentHistoryView(APIView):
    def get(self, request):
        students = set(Payment.objects.values_list('student', flat=True))
        payment_history = []

        for student in students:
            payments = Payment.objects.filter(student=student)
            serialized_data = StudentPaymentHistorySerializer({
                'student': User.objects.get(pk=student).email,
                # 'student': student,
                'payments': payments
            }).data
            payment_history.append(serialized_data)

        return Response(payment_history)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_pk = self.kwargs.get('course_pk')
        serializer = self.get_serializer(data={'user': request.user.pk, 'course': course_pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'You have subscribed for the course'}, status=status.HTTP_201_CREATED)


class SubscriptionDeleteAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'course_pk'

    def get_object(self):
        course_pk = self.kwargs.get('course_pk')
        user_pk = self.request.user.pk
        queryset = Subscription.objects.filter(user__pk=user_pk, course__pk=course_pk)
        return get_object_or_404(queryset)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'You have unsubscribed for the course'}, status=status.HTTP_204_NO_CONTENT)
