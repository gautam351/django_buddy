from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class UserModel(models.Model):
    # creating role choices
    ROLE_CHOICES = (
         ('admin', 'Admin'),
         ('edge', 'Edge'),
     )
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=55)
    email=models.EmailField(unique=True)
    password=models.BinaryField(max_length=500)
    is_verified=models.BooleanField(default=False)
    date_created=models.DateTimeField(default=timezone.now)
    is_active=models.BooleanField(default=True)
    otp=models.CharField(default="",max_length=6)
    otpExpire=models.DateTimeField(default=None,null=True,blank=True)
    is_two_factor_auth_enabled=models.BooleanField(default=False)
    deleted_date=models.DateTimeField(default=None,null=True,blank=True)
    role=models.CharField(choices=ROLE_CHOICES,default="edge",max_length=6)
    incorrect_attemps=models.SmallIntegerField(default=0)
    locked_time=models.DateTimeField(default=None,blank=True,null=True)