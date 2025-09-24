from rest_framework import serializers
from .models import User
import bcrypt


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        raw_password = validated_data.pop("password")
        saved_pw = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
        validated_data["password"] = saved_pw.decode("utf-8")
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_id = data.get("user_id")
        password = data.get("password")

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("아이디나 비밀번호가 올바르지 않습니다.")

        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            raise serializers.ValidationError("아이디나 비밀번호가 올바르지 않습니다.")

        data["user"] = user
        return data
