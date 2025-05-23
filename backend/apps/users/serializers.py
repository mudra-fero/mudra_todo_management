from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User, UserProfile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "id"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ["username", "password", "email", "role"]

    def create(self, validated_data):
        user = {
            "username": validated_data.pop("username"),
            "email": validated_data.pop("email"),
            "password": validated_data.pop("password"),
        }
        user_serializer = CustomUserSerializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return UserProfile.objects.create(user=user, **validated_data)


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
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    assigned_tasks = serializers.SerializerMethodField()
    collaborated_tasks = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "email",
            "role",
            "assigned_tasks",
            "collaborated_tasks",
        ]
        read_only_fields = ["id", "assigned_tasks", "collaborated_tasks"]

    def get_assigned_tasks(self, obj):
        return obj.assigned_tasks.count()

    def get_collaborated_tasks(self, obj):
        return obj.task_collaborations.values("task").distinct().count()

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user_serializer = CustomUserSerializer(
            instance=instance.user, data=user_data, partial=True
        )
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self):
        user = self.context["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
