from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.ReadOnlyField(source="is_staff")
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = [
            "id",
            "username",
            "email",
            "name",
            "isAdmin",
            "is_verified",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exist():
            raise serializers.ValidationError("User not found")
        return email

    def validate_otp(self, otp, email):
        user = User.objects.filter(email=email).first()
        if user.otp != otp:
            raise serializers.ValidationError("Invalid OTP provided.")
        return otp
