from rest_framework import serializers
from .models import UserModel

class userModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields=["id","name","email","is_verified","date_created","is_active","is_two_factor_auth_enabled","role"]
        # fields="__all__"