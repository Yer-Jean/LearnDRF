from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from courses.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    #  Вывод в списке уроков названия курса, а не его id
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'  # ('title', 'description',)`


class CourseSerializer(serializers.ModelSerializer):
    # Можно сделать так:
    # lessons = LessonSerializer(source='lesson_set', many=True)
    # lessons_count = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    # но из-за указания related_name='lessons' в модели Lesson сделаем так:
    lessons_count = serializers.IntegerField(source='lessons.all.count', read_only=True)
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'  # ('title', 'description',)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentHistorySerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    lesson = SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())
    payment_type = serializers.CharField(source='get_payment_type_display', read_only=True)

    class Meta:
        model = Payment
        fields = ('payment_date', 'amount', 'payment_type', 'course', 'lesson')


class StudentPaymentHistorySerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'student': instance['student'],
            'payments': PaymentHistorySerializer(instance['payments'], many=True).data
        }
