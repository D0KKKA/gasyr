# Generated by Django 5.0 on 2024-04-02 04:32

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_phone_phone_number_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1924, 4, 27)), django.core.validators.MaxValueValidator(datetime.date(2024, 4, 2))]),
        ),
    ]