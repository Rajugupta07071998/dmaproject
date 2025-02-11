from django.contrib import admin

from core.models import BusinessInfo, PersonalInfo

# Register your models here.


admin.site.register(PersonalInfo)
admin.site.register(BusinessInfo)
