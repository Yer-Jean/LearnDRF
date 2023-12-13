from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

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
