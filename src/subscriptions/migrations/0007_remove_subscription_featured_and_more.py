# Generated by Django 5.0.9 on 2024-10-11 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_subscription_featured_subscription_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='featured',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='order',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='updated',
        ),
    ]
