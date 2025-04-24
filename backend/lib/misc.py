def join_usernames(queryset):
    return ", ".join([str(item.user.username) for item in queryset])
