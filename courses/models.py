from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=300, verbose_name='Title')
    preview = models.ImageField(upload_to='courses/', verbose_name='Preview', **NULLABLE)
    description = models.TextField(verbose_name='Description', **NULLABLE)

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

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('cash', 'Paid in cash'),
        ('card', 'Paid by card')
    )
    student = models.CharField(max_length=150, verbose_name='Student')
    payment_date = models.DateField(verbose_name='Date of payment')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Lesson', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='Amount')
    payment_type = models.CharField(choices=PAYMENT_TYPE_CHOICES, verbose_name="Payment Type")
