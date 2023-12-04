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
    lessons_count = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    # Можно сделать так:
    # lessons = LessonSerializer(source='lesson_set', many=True)
    # но из-за указания related_name='lessons' в модели Lesson сделаем так:
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'  # ('title', 'description',)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
