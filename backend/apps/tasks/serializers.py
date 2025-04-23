from rest_framework import serializers
from .models import Task
from apps.users.models import User


class CreateTaskSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "lifecycle_stage",
            "priority",
            "deadline",
        )


class AssignTaskSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

    def validate_user_ids(self, value):
        users = User.objects.filter(id__in=value)
        if users.count() != len(value):
            raise serializers.ValidationError("One or more user IDs are invalid.")
        return users

    def save(self, **kwargs):
        task = self.context["task"]
        users = self.validated_data["user_ids"]
        task.assigned_to.set(users)
        return task


class CollaboratorTaskSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["add", "remove"])
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

    def validate_user_ids(self, value):
        users = User.objects.filter(id__in=value)
        if users.count() != len(value):
            raise serializers.ValidationError("One or more user IDs are invalid.")
        return users

    def save(self, **kwargs):
        task = self.context["task"]
        users = self.validated_data["user_ids"]
        action = self.validated_data["action"]

        if action == "add":
            task.collaborators.add(*users)
        else:
            task.collaborators.remove(*users)
        return task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        depth = 2
        fields = "__all__"
