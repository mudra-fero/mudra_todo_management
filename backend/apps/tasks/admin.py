from django.contrib import admin, messages

from lib.misc import join_usernames
from .models import Task, TaskCollaborator


class TaskCollaborationInline(admin.TabularInline):
    model = TaskCollaborator
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "priority",
        "lifecycle_stage",
        "deadline",
        "created_by",
        "get_collaborators",
        "get_assigned_users",
    )
    list_filter = ("priority", "lifecycle_stage", "deadline")
    search_fields = ("title", "description", "created_by__username")
    ordering = ("-deadline",)
    inlines = [TaskCollaborationInline]
    actions = ["mark_as_completed", "change_priority_to_critical"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "priority",
                    "lifecycle_stage",
                    "deadline",
                )
            },
        ),
        ("User Assignment", {"fields": ("created_by",)}),
    )

    def get_collaborators(self, obj):
        return join_usernames(obj.task_collaborations.all())

    get_collaborators.short_description = "Collaborators"

    def get_assigned_users(self, obj):
        return join_usernames(obj.task_assignments.all())

    get_assigned_users.short_description = "Assigned users"

    def mark_as_completed(modeladmin, request, queryset):
        updated = queryset.update(lifecycle_stage=3)
        modeladmin.message_user(
            request, f"{updated} task(s) marked as completed.", messages.SUCCESS
        )

    mark_as_completed.short_description = "Mark selected tasks as completed"

    def change_priority_to_critical(modeladmin, request, queryset):
        updated = queryset.update(priority=4)
        modeladmin.message_user(
            request, f"{updated} task(s) priority has changed.", messages.SUCCESS
        )

    mark_as_completed.short_description = "Mark selected tasks as completed"
