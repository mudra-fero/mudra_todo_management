from rest_framework import serializers
from .models import Task, TaskAssignment, TaskCollaborator
from ..users.models import User


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


class AssignTaskSerializer(serializers.ModelSerializer):
    user_ids = serializers.ListSerializer(
        allow_null=False, child=serializers.IntegerField()
    )

    def create(self, validated_data):
        task = self.context["task"]
        users = [User.objects.get(id=user_id) for user_id in validated_data["user_ids"]]
        TaskAssignment.objects.filter(task=task).delete()
        return TaskAssignment.objects.bulk_create(
            [TaskAssignment(task=task, user=user) for user in users]
        )

    class Meta:
        model = TaskAssignment
        fields = ["task", "user_ids"]


class CollaboratorTaskSerializer(serializers.ModelSerializer):
    user_ids = serializers.ListSerializer(
        allow_null=False, child=serializers.IntegerField()
    )

    def create(self, validated_data):
        task = self.context["task"]
        users = [User.objects.get(id=user_id) for user_id in validated_data["user_ids"]]
        TaskCollaborator.objects.filter(task=task).delete()
        return TaskCollaborator.objects.bulk_create(
            [TaskCollaborator(task=task, user=user) for user in users]
        )

    class Meta:
        model = TaskCollaborator
        fields = ["task", "user_ids"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        depth = 2
        fields = "__all__"
