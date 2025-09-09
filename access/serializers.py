from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password

from .models import (
    CustomUserModel,
    EmailConfirmationControl,
    LoggedDevice,
    PasswordRecoveryEmail,
    PreRegister,
    ResetPasswordControl,
)


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUserModel
        fields = (
            "userId",
            "username",
            "email",
            "avatar",
            "phone_number",
            "birth_date",
            "dalle_credits",
            "subscription_credits",
            "is_email_confirmed",
            "notification_settings",
            "created",
            "updated",
            "password",
            "password_confirm",
        )
        read_only_fields = (
            "userId",
            "created",
            "updated",
            "dalle_credits",
            "subscription_credits",
        )

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password_confirm"):
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm", None)
        password = validated_data.pop("password")
        user = CustomUserModel.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop("password_confirm", None)
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class CustomUserListSerializer(serializers.ModelSerializer):
    """Simplified serializer for user lists"""

    class Meta:
        model = CustomUserModel
        fields = ("userId", "username", "email", "is_email_confirmed", "created")


class ResetPasswordControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPasswordControl
        fields = "__all__"
        read_only_fields = ("request_id", "date")


class PasswordRecoveryEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordRecoveryEmail
        fields = (
            "id",
            "name",
            "body",
            "subject",
            "email_adress",
        )


class EmailConfirmationControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmationControl
        fields = "__all__"
        read_only_fields = ("date",)


class PreRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreRegister
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "date")


class LoggedDeviceSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = LoggedDevice
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "last_login_at", "user")

    def validate(self, attrs):
        # Get user from context (set by the view)
        user = self.context["request"].user if "request" in self.context else None
        device_type = attrs.get("device_type")
        device_name = attrs.get("device_name")

        # Check for existing device with same user, type, and name
        if (
            user
            and LoggedDevice.objects.filter(
                user=user, device_type=device_type, device_name=device_name
            ).exists()
        ):
            raise serializers.ValidationError(
                "Device with this user, type, and name already exists."
            )
        return attrs
