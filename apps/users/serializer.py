from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.ReadOnlyField(source='is_staff')
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        extra_kwargs = {
            'password': {'write_only': True}
        }
        fields = ["id", "username", "email", "name", "isAdmin", "password", "password_confirm"]

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        print(password, password_confirm)
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


