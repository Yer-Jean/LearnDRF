# Generated by Django 4.2.7 on 2023-12-04 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_rename_payments_payment_alter_lesson_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='date',
            new_name='payment_date',
        ),
    ]
