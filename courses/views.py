from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from courses.models import Course, Lesson, Payment
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, StudentPaymentHistorySerializer
from users.models import User


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


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