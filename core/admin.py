from django.contrib import admin
from core.models import (
    PersonalInfo, BusinessInfo, MembershipRequest, BusinessMembership, 
    Notification, EquipmentMaster, Achievement, UserActivity,
    MainCategory, SubCategory, SubSubCategory
)

# **PersonalInfo Admin Panel**
@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "location", "is_active", "created_at")  
    search_fields = ("user__username", "location")  
    list_filter = ("gender", "is_active")  
    ordering = ("-created_at",)  


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "main_category", "description")
    list_filter = ("main_category",)
    search_fields = ("name",)


@admin.register(SubSubCategory)
class SubSubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sub_category", "description")
    list_filter = ("sub_category",)
    search_fields = ("name",)


# **BusinessInfo Admin Panel**
@admin.register(BusinessInfo)
class BusinessInfoAdmin(admin.ModelAdmin):
    list_display = (
        "user", "business_name", "main_category", "sub_category", "sub_sub_category", "business_phone"
    )
    list_filter = ("main_category", "sub_category", "sub_sub_category")
    search_fields = ("business_name", "user__username", "business_phone")

    fieldsets = (
        ("Business Owner", {"fields": ("user",)}),
        ("Category Details", {"fields": ("main_category", "sub_category", "sub_sub_category")}),
        ("Business Details", {"fields": ("business_name", "business_about", "business_description")}),
        ("Contact Information", {"fields": ("business_address", "business_phone", "business_website")}),
    )


# **MembershipRequest Admin Panel**
@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "business", "status", "created_at")  
    search_fields = ("user__username", "business__business_name")  
    list_filter = ("status", "created_at")  
    actions = ["accept_requests", "reject_requests"]  

    def accept_requests(self, request, queryset):
        queryset.update(status='accepted')
    accept_requests.short_description = "Mark selected requests as accepted"

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')
    reject_requests.short_description = "Mark selected requests as rejected"

# **BusinessMembership Admin Panel**
@admin.register(BusinessMembership)
class BusinessMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "business", "joined_at")  
    search_fields = ("user__username", "business__business_name")  
    list_filter = ("joined_at",)  
    ordering = ("-joined_at",)  

# **Notification Admin Panel**
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "sender", "notification_type", "is_read", "created_at")  
    search_fields = ("recipient__username", "sender__username", "message")  
    list_filter = ("notification_type", "is_read")  
    ordering = ("-created_at",)  
    actions = ["mark_as_read"]

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected notifications as read"

# **EquipmentMaster Admin Panel**
@admin.register(EquipmentMaster)
class EquipmentMasterAdmin(admin.ModelAdmin):
    list_display = ("name", "no_of_equipment", "is_system", "created_by", "created_at")  
    search_fields = ("name", "description")  
    list_filter = ("is_system", "created_by")  
    ordering = ("-created_at",)  

# **Achievement Admin Panel**
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "business", "date_awarded", "created_at")  
    search_fields = ("title", "business__business_name")  
    list_filter = ("date_awarded",)  
    ordering = ("-date_awarded",)  


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for UserActivity model.
    Displays key fields and enables search & filtering.
    """

    list_display = ('user', 'ip_address', 'location', 'device_type', 'os', 'browser', 'created_at')
    search_fields = ('user__username', 'ip_address', 'location', 'device_type', 'os', 'browser')
    list_filter = ('device_type', 'os', 'browser', 'created_at')
    ordering = ('-created_at',)
