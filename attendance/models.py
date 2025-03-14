from django.db import models
from core.models import BaseModel
from account.models import User


class WeeklyPlan(BaseModel):
    """
    Weekly training or learning plan.

    Attributes:
        - `name` (CharField): Unique name of the weekly plan.
        - `description` (TextField): Description of the plan.
        - `start_date` (DateField): Start date of the plan.
        - `end_date` (DateField): End date of the plan.
        - Boolean fields for each day to indicate class availability.
    """

    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    is_system = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="weekly_plans"
    )  # Only business users create plans

    def __str__(self):
        return self.name if self.name else "Unnamed Weekly Plan"



class SubTask(BaseModel):
    """
    Sub-tasks linked to WeeklyPlan, assigned to specific days.

    Attributes:
        - `weekly_plan` (ForeignKey): Links the sub-task to a WeeklyPlan.
        - `day` (CharField): Specifies the day of the week (Monday-Sunday).
        - `task_name` (CharField): Name of the sub-task.
        - `duration_minutes` (IntegerField): Duration of the task in minutes.
    """

    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    weekly_plan = models.ForeignKey(
        WeeklyPlan, on_delete=models.CASCADE, related_name="sub_tasks"
    )
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    task_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField(default=30)  # Default 30 min per task

    is_system = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sub_tasks"
    )  # Only business users create sub-tasks

    def __str__(self):
        return f"{self.day.capitalize()} - {self.task_name} ({self.duration_minutes} min)"



class Batch(BaseModel):
    """
    Represents a batch that is assigned a WeeklyPlan.

    Attributes:
        - `name` (CharField): Name of the batch.
        - `weekly_plan` (ForeignKey): References a WeeklyPlan.
        - `start_time` (TimeField): Batch start time.
        - `end_time` (TimeField): Batch end time.
        - `duration_minutes` (IntegerField): Duration in minutes.
    """

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    weekly_plan = models.ForeignKey(
        WeeklyPlan, on_delete=models.CASCADE, related_name="batches", blank=True, null=True
    )
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)  # Auto-calculated if start & end time exist

    is_system = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="batches"
    )  # Only business users create batches

    def save(self, *args, **kwargs):
        """Auto-calculate duration based on start and end time."""
        if self.start_time and self.end_time:
            from datetime import datetime
            fmt = "%H:%M:%S"
            start = datetime.strptime(str(self.start_time), fmt)
            end = datetime.strptime(str(self.end_time), fmt)
            self.duration_minutes = (end - start).seconds // 60  # Convert seconds to minutes
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else "Unnamed Batch"



class MasterPolicy(BaseModel):
    """
    Master Policy attached to a batch.

    Attributes:
        - `batch` (ForeignKey): Links the policy to a Batch.
    """

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    batch = models.ForeignKey(
        Batch, on_delete=models.CASCADE, related_name="batch_policies", blank=True, null=True
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="master_policies"
    )  # Only business users create policies

    def __str__(self):
        return f"MasterPolicy for {self.batch.name}" if self.batch else "Unassigned Policy"



class Attendance(BaseModel):
    """
    Attendance model to track student attendance batch-wise.

    Attributes:
        - `batch` (ForeignKey): References the Batch.
        - `user` (ForeignKey): References the User.
        - `date` (DateField): Date of the attendance entry.
        - `status` (CharField): Status of attendance (Present, Absent, Leave, Holiday).
    """

    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
        ('holiday', 'Holiday'),
    ]

    batch = models.ForeignKey(
        Batch, on_delete=models.CASCADE, related_name="attendance_records", blank=True, null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attendance", blank=True, null=True
    )
    date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='present', blank=True, null=True
    )

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recorded_attendance"
    )  # Business user who marks attendance

    # class Meta:
    #     unique_together = ('batch', 'user', 'date')  # Ensures unique attendance record per user per day

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date} - {self.status}" if self.user and self.date else "Attendance Entry"
