# Generated by Django 5.0.9 on 2024-10-16 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_alter_customer_first_name_alter_customer_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
