# Generated by Django 4.2.4 on 2023-08-03 15:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('is_verified', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(default=datetime.datetime(2023, 8, 3, 20, 46, 13, 900786))),
                ('is_active', models.BooleanField(default=True)),
                ('otp', models.CharField(default='', max_length=6)),
                ('is_two_factor_auth_enabled', models.BooleanField(default=False)),
                ('deleted_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('edge', 'Edge')], default='edge', max_length=6)),
                ('incorrect_attemps', models.SmallIntegerField(default=0)),
                ('locked_time', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
    ]