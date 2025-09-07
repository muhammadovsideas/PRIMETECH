from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username',  'first_name', 'last_name','phone_number',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ('id', 'username', 'password',  'first_name', 'last_name')

    def create(self,validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user