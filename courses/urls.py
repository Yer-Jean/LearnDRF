from django.urls import path
from courses.apps import CoursesConfig
from rest_framework.routers import DefaultRouter

from courses.views import *

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment_history/', StudentPaymentHistoryView.as_view(), name='student_payment_history'),

    path('payment/create_by_card/', PaymentByCardCreateAPIView.as_view(), name='payment_by_card_create'),
    path('payment/get_by_card/', PaymentByCardGetAPIView.as_view(), name='payment_by_card_get'),
    # path('payment/<str:session_id>/', PaymentByCardGetAPIView.as_view(), name='payment_by_card_get'),

    path('subscribe/<int:course_pk>/', SubscriptionCreateAPIView.as_view(), name='course_subscribe'),
    path('unsubscribe/<int:course_pk>/', SubscriptionDeleteAPIView.as_view(), name='course_unsubscribe'),
] + router.urls
