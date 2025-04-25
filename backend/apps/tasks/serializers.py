from rest_framework import serializers
from .models import Task, TaskAssignment, TaskCollaborator, Comment, TaskHistory
from ..users.models import User


class CreateTaskSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        task = Task.objects.create(**validated_data)

        TaskHistory.objects.create(
            task=task, user=self.context["request"].user, action="Created task"
        )
        return task

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        TaskHistory.objects.create(
            task=instance, user=self.context["request"].user, action="Updated task"
        )
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
        TaskHistory.objects.create(
            task=task,
            user=self.context["request"].user,
            action=f"Assigned users: {', '.join([user.username for user in users])}",
        )
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
        TaskHistory.objects.create(
            task=task,
            user=self.context["request"].user,
            action=f"Added collaborators: {', '.join([user.username for user in users])}",
        )
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


class CommentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context["request"]
        task = self.context["task"]
        TaskHistory.objects.create(
            task=task,
            user=request.user,
            action=f"Added comment: {validated_data['content']}",
        )
        return Comment.objects.create(task=task, author=request.user, **validated_data)

    class Meta:
        model = Comment
        depth = 2
        fields = ["id", "content", "author", "created_at"]
        read_only_fields = ["created_at", "author", "id"]


class TaskHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskHistory
        depth = 2
        fields = ["id", "user", "action", "timestamp"]
