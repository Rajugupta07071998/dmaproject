from django.urls import path
from .views import (
    WeeklyPlanAPIView, WeeklyPlanDetailAPIView,
    SubTaskAPIView, SubTaskDetailAPIView,
    BatchAPIView, BatchDetailAPIView,
    MasterPolicyAPIView, MasterPolicyDetailAPIView, 
    BatchAttendanceAPIView, AssignBatchAPIView,
    BatchWiseMembersAPIView, AttendanceReportAPIView,
    UserAttendanceAPIView, AttendanceLogsAPIView
)

urlpatterns = [
    # List & Create
    path('weekly-plans/', WeeklyPlanAPIView.as_view(), name='weekly-plans'),
    path('sub-tasks/', SubTaskAPIView.as_view(), name='sub-tasks'),
    path('batches/', BatchAPIView.as_view(), name='batches'),
    path('master-policies/', MasterPolicyAPIView.as_view(), name='master-policies'),
    #path('attendance/', AttendanceAPIView.as_view(), name='attendance'),

    # Single Retrieve, Update, Delete
    path('weekly-plans/<pk>/', WeeklyPlanDetailAPIView.as_view(), name='weekly-plan-detail'),
    path('sub-tasks/<pk>/', SubTaskDetailAPIView.as_view(), name='sub-task-detail'),
    path('batches/<pk>/', BatchDetailAPIView.as_view(), name='batch-detail'),
    path('master-policies/<pk>/', MasterPolicyDetailAPIView.as_view(), name='master-policy-detail'),
    #path('attendance/<pk>/', AttendanceDetailAPIView.as_view(), name='attendance-detail'),
    path('batch/<batch_id>/attendance/', BatchAttendanceAPIView.as_view(), name='batch-attendance'),
    path("assign-batch/<user_id>/<batch_id>/", AssignBatchAPIView.as_view(), name="assign_batch"),
    path('batch-members/<batch_id>/', BatchWiseMembersAPIView.as_view(), name='batch-wise-members'),
    path('attendance-report/', AttendanceReportAPIView.as_view(), name='attendance-report'),
    path('attendance/user/<user_id>/', UserAttendanceAPIView.as_view(), name='user-attendance'),
    path('batch/<batch_id>/attendance/logs/', AttendanceLogsAPIView.as_view(), name='attendance-logs'), # last 2 



]
