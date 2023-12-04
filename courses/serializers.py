from rest_framework import serializers

from courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lesson_set.all.count', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'  # ('title', 'description',)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'  # ('title', 'description',)`
