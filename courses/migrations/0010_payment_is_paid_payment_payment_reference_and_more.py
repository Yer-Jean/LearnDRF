# Generated by Django 4.2.7 on 2023-12-17 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Paid'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_reference',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Payment Reference'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'Paid in cash'), ('bank', 'Bank Transfer'), ('card', 'Paid by card')], verbose_name='Payment Type'),
        ),
    ]
