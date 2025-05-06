import datetime

from rest_framework import serializers
from .models import Task, TaskCollaborator, Comment, TaskHistory
from ..users.models import UserProfile


class CreateTaskSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user.profile
        task = Task.objects.create(**validated_data)

        TaskHistory.objects.create(
            task=task,
            user=self.context["request"].user.profile,
            action="Created task",
        )
        return task

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        TaskHistory.objects.create(
            task=instance,
            user=self.context["request"].user.profile,
            action="Updated task",
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


class AssignTaskSerializer(serializers.Serializer):
    user_ids = serializers.IntegerField()

    def create(self, validated_data):
        task = self.context["task"]
        profile = UserProfile.objects.get(id=validated_data["user_ids"])
        TaskHistory.objects.create(
            task=task,
            user=self.context["request"].user.profile,
            action=f"Assigned users: {profile.user.username}",
        )
        task.assigned_to = profile if profile else None
        task.assigned_at = datetime.date.today()
        task.save()
        return task


class CollaboratorTaskSerializer(serializers.Serializer):
    user_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), allow_null=False
    )

    def create(self, validated_data):
        task = self.context["task"]
        users = [
            UserProfile.objects.get(id=user_id)
            for user_id in validated_data["user_ids"]
        ]

        TaskCollaborator.objects.filter(task=task).delete()
        TaskCollaborator.objects.bulk_create(
            [TaskCollaborator(task=task, user=user) for user in users]
        )

        TaskHistory.objects.create(
            task=task,
            user=self.context["request"].user.profile,
            action=f"Added collaborators: {', '.join([u.user.username for u in users])}",
        )
        return task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        depth = 2
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context["request"]
        task = self.context["task"]
        author_profile = request.user.profile
        TaskHistory.objects.create(
            task=task,
            user=author_profile,
            action=f"Added comment: {validated_data['content']}",
        )
        return Comment.objects.create(
            task=task, author=author_profile, **validated_data
        )

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
