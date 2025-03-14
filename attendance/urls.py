from django.urls import path
from .views import (
    WeeklyPlanAPIView, WeeklyPlanDetailAPIView,
    SubTaskAPIView, SubTaskDetailAPIView,
    BatchAPIView, BatchDetailAPIView,
    MasterPolicyAPIView, MasterPolicyDetailAPIView, 
    BatchAttendanceAPIView
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

]
