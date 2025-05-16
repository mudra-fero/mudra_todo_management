from datetime import datetime

from django.utils.timezone import make_aware, get_current_timezone
from rest_framework import serializers
from .models import Task, TaskCollaborator, Comment, TaskHistory, Notification
from ..users.models import UserProfile
from ..users.serializers import UserSerializer
from django.contrib.humanize.templatetags.humanize import naturaltime


class CreateTaskSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user.profile
        task = super().create(validated_data)
        task.add_history(
            task=task, user=self.context["request"].user.profile, message="Created task"
        )
        task.add_notification(
            task=task,
            acting_user=self.context["request"].user.profile,
            message="Created task",
        )
        return task

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.add_history(
            task=instance,
            user=self.context["request"].user.profile,
            message="Updated task",
        )
        instance.add_notification(
            task=instance,
            acting_user=self.context["request"].user.profile,
            message="Updated task",
        )
        return instance


class AssignTaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Task
        fields = ["user_id"]

    def create(self, validated_data):
        task = self.context["task"]
        profile = UserProfile.objects.get(id=validated_data["user_id"])
        task.assigned_to = profile if profile else None
        task.save()
        task.add_history(
            task=task,
            user=self.context["request"].user.profile,
            message=f"Assigned user: {profile.user.username}",
        )
        task.add_notification(
            task=task,
            acting_user=self.context["request"].user.profile,
            message=f"Assigned user: {profile.user.username}",
        )
        return task


class CollaboratorTaskSerializer(serializers.ModelSerializer):
    user_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), allow_null=False
    )

    class Meta:
        model = Task
        fields = ["user_ids"]

    def create(self, validated_data):
        task = self.context["task"]
        users = UserProfile.objects.filter(id__in=validated_data["user_ids"])
        TaskCollaborator.objects.filter(task=task).delete()
        TaskCollaborator.objects.bulk_create(
            [TaskCollaborator(task=task, user=user) for user in users]
        )
        task.add_history(
            task=task,
            user=self.context["request"].user.profile,
            message=f"Added collaborators: {', '.join([u.user.username for u in users])}",
        )
        task.add_notification(
            task=task,
            acting_user=self.context["request"].user.profile,
            message=f"Added collaborators: {', '.join([u.user.username for u in users])}",
        )
        return task


class TaskCollaboratorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TaskCollaborator
        fields = ("user",)


class TaskSerializer(serializers.ModelSerializer):
    collaborated_with = serializers.SerializerMethodField()
    deadline_humanized = serializers.SerializerMethodField()
    created_humanized = serializers.SerializerMethodField()

    class Meta:
        model = Task
        depth = 2
        fields = "__all__"

    def get_collaborated_with(self, obj):
        collaborators = obj.task_collaborations.all()
        return TaskCollaboratorSerializer(
            collaborators, many=True, context=self.context
        ).data

    def get_deadline_humanized(self, obj):
        if obj.deadline:
            dt = datetime.combine(obj.deadline, datetime.min.time())
            aware_dt = make_aware(dt, timezone=get_current_timezone())
            return naturaltime(aware_dt)
        return None

    def get_created_humanized(self, obj):
        if obj.created:
            dt = datetime.combine(obj.created, datetime.min.time())
            aware_dt = make_aware(dt, timezone=get_current_timezone())
            return naturaltime(aware_dt)
        return None


class CommentSerializer(serializers.ModelSerializer):
    created_humanized = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        depth = 2
        fields = ["id", "content", "author", "created", "created_humanized"]
        read_only_fields = ["created", "author", "id", "created_humanized"]

    def get_created_humanized(self, obj):
        if obj.created:
            dt = datetime.combine(obj.created, datetime.min.time())
            aware_dt = make_aware(dt, timezone=get_current_timezone())
            return naturaltime(aware_dt)
        return None

    def create(self, validated_data):
        request = self.context["request"]
        task = self.context["task"]
        author_profile = request.user.profile
        task.add_history(
            task=task,
            user=self.context["request"].user.profile,
            message=f"Added comment: {validated_data['content']}",
        )
        task.add_notification(
            task=task,
            acting_user=self.context["request"].user.profile,
            message=f"Added comment: {validated_data['content']}",
        )
        return Comment.objects.create(
            task=task, author=author_profile, **validated_data
        )


class TaskHistorySerializer(serializers.ModelSerializer):
    created_humanized = serializers.SerializerMethodField()

    def get_created_humanized(self, obj):
        if obj.created:
            dt = datetime.combine(obj.created, datetime.min.time())
            aware_dt = make_aware(dt, timezone=get_current_timezone())
            return naturaltime(aware_dt)
        return None

    class Meta:
        model = TaskHistory
        depth = 2
        fields = ["id", "user", "action", "created", "created_humanized"]
        read_only_fields = ["id", "created_humanized"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "message", "is_read", "created", "modified"]
