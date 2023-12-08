from django.contrib import admin

from courses.models import Course, Lesson, Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner')
    list_filter = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'course', 'owner')
    list_filter = ('title',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'payment_date', 'course', 'lesson', 'amount', 'payment_type')
    list_filter = ('student',)
