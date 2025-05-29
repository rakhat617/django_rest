from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "first_name", 
            "last_name", "email", "password"
        ]
        # exclude = ["password", "groups", "user_permissions"]

    def save(self, **kwargs):
        raw_password: str | None = kwargs.get("password")
        if raw_password:
            kwargs["password"] = make_password(password=raw_password)
        return super().save(**kwargs)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=50
    )

#     def validate(self, attrs):
#         if len(attrs) < 8:
#             raise ValueError
#         return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_conf = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not check_password(password=value, encoded=user.password):
            raise serializers.ValidationError("Неверный текущий пароль. Попробуйте снова")
        return value

    def validate(self, data):
        if data["new_password"] != data["new_password_conf"]:
            raise serializers.ValidationError("Пароли не совпадают. Попробуйте снова")
        return data


