from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=300, verbose_name='Title')
    preview = models.ImageField(upload_to='courses/', verbose_name='Preview', **NULLABLE)
    description = models.TextField(verbose_name='Description', **NULLABLE)


class Lesson(models.Model):
    title = models.CharField(max_length=300, verbose_name='Title')
    preview = models.ImageField(upload_to='courses/', verbose_name='Preview', **NULLABLE)
    description = models.TextField(verbose_name='Description', **NULLABLE)
    video_url = models.URLField(verbose_name='Link to video', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
