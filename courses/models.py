from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=300, verbose_name='Title')
    preview = models.ImageField(upload_to='courses/', verbose_name='Preview', **NULLABLE)
    description = models.TextField(verbose_name='Description', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Lesson(models.Model):
    title = models.CharField(max_length=300, verbose_name='Title')
    preview = models.ImageField(upload_to='courses/', verbose_name='Preview', **NULLABLE)
    description = models.TextField(verbose_name='Description', **NULLABLE)
    video_url = models.URLField(verbose_name='Link to video', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('cash', 'Paid in cash'),
        ('bank', 'Bank Transfer')
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                **NULLABLE, verbose_name='Student')
    payment_date = models.DateField(verbose_name='Date of payment')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Lesson', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='Amount')
    payment_type = models.CharField(choices=PAYMENT_TYPE_CHOICES, verbose_name="Payment Type")


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
