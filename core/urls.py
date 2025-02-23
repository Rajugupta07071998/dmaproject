from django.urls import path
from .views import *

urlpatterns = [
    # Personal Info
    path('personal-info/', PersonalInfoAPIView.as_view(), name='personal-info-create'),
    path('personal-info/<pk>/', PersonalInfoAPIView.as_view(), name='personal-info'),
    
    # Business Info
    path('business-info/', BusinessInfoAPIView.as_view(), name='business-info-create'),
    path('business-info/<pk>/', BusinessInfoAPIView.as_view(), name='business-info'),
    
    # Achievements
    path('achievements/', AchievementListCreateAPIView.as_view(), name='achievement-list-create'),
    path('achievements/<id>/', AchievementDetailAPIView.as_view(), name='achievement-detail'),

    # Notification
    path('notifications/', NotificationAPIView.as_view(), name='notifications'),
    path('notifications/<notification_id>/read/', NotificationAPIView.as_view(), name='notification-read'),
]
