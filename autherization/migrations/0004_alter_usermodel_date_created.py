# Generated by Django 4.2.4 on 2023-08-06 12:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autherization', '0003_alter_usermodel_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 12, 16, 23, 603083, tzinfo=datetime.timezone.utc)),
        ),
    ]
