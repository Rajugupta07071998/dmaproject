from django.contrib import admin

from core.models import BusinessInfo, PersonalInfo, MembershipRequest, BusinessMembership, Notification

# Register your models here.


admin.site.register(PersonalInfo)
admin.site.register(BusinessInfo)
admin.site.register(MembershipRequest)
admin.site.register(BusinessMembership)
admin.site.register(Notification)

