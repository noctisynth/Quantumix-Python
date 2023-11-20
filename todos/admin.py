from django.contrib import admin

from .models import Permission, User, Project, Todo, Task


@admin.register(Permission)
class PermissionsAdmin(admin.ModelAdmin):
    list_filter = ["name", "level"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ["permission"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_filter = ["permission", "priority", "is_checked"]


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_filter = ["permission", "priority", "is_checked"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ["permission", "priority", "is_checked"]
