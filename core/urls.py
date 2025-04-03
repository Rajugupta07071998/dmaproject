from django.urls import path
from .views import *

urlpatterns = [
    # Personal Info
    path('personal-info/', PersonalInfoAPIView.as_view(), name='personal-info-create'),
    path('personal-info/<pk>/', PersonalInfoAPIView.as_view(), name='personal-info'),
    
    # Business Info
    path('business-info/', BusinessInfoAPIView.as_view(), name='business-info-create'),
    path('categories/', MainCategoryListAPIView.as_view(), name='main-category-list'),
    path('categories/<main_category_id>/subcategories/', SubCategoryListAPIView.as_view(), name='sub-category-list'),
    path('categories/<sub_category_id>/subsubcategories/', SubSubCategoryListAPIView.as_view(), name='sub-sub-category-list'),
    path('business-info/<pk>/', BusinessInfoAPIView.as_view(), name='business-info'),
    path('business/search/', BusinessSearchView.as_view(), name='business-search'),
    path('business/<business_id>/', BusinessDetailView.as_view(), name='business-detail'),

    # Membership
    path('business/join-request/', BusinessJoinRequestView.as_view(), name='business-join-request'),
    path('business/approve-request/<request_id>/', ApproveMembershipRequestView.as_view(), name='approve-request'),
    path('business/my-memberships/<user_id>/', MyBusinessMembershipsView.as_view(), name='my-memberships'),
    
    # Achievements
    path('achievements/', AchievementListCreateAPIView.as_view(), name='achievement-list-create'),
    path('achievements/<id>/', AchievementDetailAPIView.as_view(), name='achievement-detail'),

    # Notification
    path('notifications/', NotificationAPIView.as_view(), name='notifications'),
    path('notifications/<notification_id>/read/', NotificationAPIView.as_view(), name='notification-read'),

    path('equipment/', EquipmentMasterAPIView.as_view(), name='equipment-list'),
    path('equipment/<equipment_id>/', EquipmentMasterAPIView.as_view(), name='equipment-detail'),

    path('business/members/<business_id>/', BusinessMembersListView.as_view(), name='business-members'),
    path('user/details/<user_id>/', UserDetailsView.as_view(), name='user-details'),
    path("update-privacy/", UpdatePrivacyAPIView.as_view(), name="update-privacy"),
    path('user-activities/<user_id>/', UserActivityAPIView.as_view(), name='user-activities'),
]
