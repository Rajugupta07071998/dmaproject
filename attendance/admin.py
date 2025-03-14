from django.contrib import admin
from .models import WeeklyPlan, SubTask, Batch, MasterPolicy, Attendance


@admin.register(WeeklyPlan)
class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "created_by")
    search_fields = ("name", "created_by__username")
    list_filter = ("start_date", "end_date")
    ordering = ("start_date",)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("weekly_plan", "day", "task_name", "duration_minutes", "created_by")
    search_fields = ("task_name", "weekly_plan__name")
    list_filter = ("day",)
    ordering = ("day",)


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("name", "weekly_plan", "start_time", "end_time", "duration_minutes", "created_by")
    search_fields = ("name", "weekly_plan__name")
    list_filter = ("start_time", "end_time")
    ordering = ("start_time",)


@admin.register(MasterPolicy)
class MasterPolicyAdmin(admin.ModelAdmin):
    list_display = ("batch", "created_by")
    search_fields = ("batch__name",)
    ordering = ("batch",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("batch", "user", "date", "status", "created_by")
    search_fields = ("user__username", "batch__name")
    list_filter = ("status", "date")
    ordering = ("date",)
