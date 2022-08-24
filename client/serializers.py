from dataclasses import fields
from rest_framework import serializers
from .models import User
from django.utils.translation import gettext as _
from .validators import PhoneValidator

class RegisterSerializer(serializers.ModelSerializer):
    confirm = serializers.CharField(max_length=120, write_only=True)
    
    def validate(self, data):
        pswrd = data.get("password")
        cnfrm = data.get("confirm")
        if pswrd != None and cnfrm != None and pswrd != cnfrm:
            raise serializers.ValidationError(_("Please confirm the password correctly!"))
        del data['confirm']
        return data

    class Meta:
        model = User
        fields = ['phone', "first_name", 'confirm', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User(
        phone=validated_data['phone'],
        first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SignInOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', "phone", "date_joined", "last_login", 'is_blocked']
        read_only_fields = ("id", 'date_joined', 'last_login', "is_blocked")


class ChangePswrdSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=35)
    new = serializers.CharField(required=True, max_length=35, write_only=True)
    confirm = serializers.CharField(required=True, max_length=35, write_only=True)

    def validate(self, data):
        error = {}
        if not self.context['request'].user.check_password(data.get("password")):
            error['password'] = "Password is not valid!"
            raise serializers.ValidationError(error)
        
        if not data.get("new") == data.get("confirm"):
            error['confirm'] = "New password confirmation is not valid!"
            raise serializers.ValidationError(error)

        return data
    
    class Meta:
        model = User
        fields = ["password", 'new', 'confirm']