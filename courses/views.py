from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from courses.permissions import IsNotModerator, IsOwner
from courses.serializers import *
from users.models import User


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):

        match self.action:
            case 'create':
                permission_classes = [IsAuthenticated, IsNotModerator]
            case 'destroy':
                permission_classes = [IsAuthenticated, IsNotModerator, IsOwner]
            case 'retrieve', 'update':
                permission_classes = [IsAuthenticated, IsOwner]
            case 'list':
                permission_classes = [IsAuthenticated, IsOwner | ~IsNotModerator]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_queryset(self):
        if self.action == 'list':
            return Course.objects.filter(owner=self.request.user)
        return super().get_queryset()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsNotModerator]

    def get_queryset(self):
        if self.request.user.groups.name != 'moderators':
            return Lesson.objects.filter(owner=self.request.user)
        return super().get_queryset()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


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