# Generated by Django 4.2.7 on 2023-12-04 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_course_options_alter_lesson_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.CharField(max_length=150, verbose_name='Student')),
                ('date', models.DateField(verbose_name='Date of payment')),
                ('amount', models.PositiveIntegerField(verbose_name='Amount')),
                ('payment_type', models.CharField(choices=[('cash', 'Paid in cash'), ('card', 'Paid by card')], verbose_name='Payment Type')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='Course')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.lesson', verbose_name='Lesson')),
            ],
        ),
    ]