from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.tasks.serializers import TaskSerializer
from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ["username", "password", "email", "role"]
        extra_kwargs = {"password": {"write_only": True}}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        raise serializers.ValidationError("Invalid credentials")

    def create(self, validated_data):
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    assigned_tasks = serializers.SerializerMethodField()
    collaborated_tasks = serializers.SerializerMethodField()

    def get_assigned_tasks(self, obj):
        return obj.assigned_tasks.count()

    def get_collaborated_tasks(self, obj):
        return obj.collaborated_tasks.count()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "assigned_tasks",
            "collaborated_tasks",
        ]
        read_only_fields = ["id", "assigned_tasks", "collaborated_tasks"]
