from django.contrib import admin


from simple_crm.models import (
    ContactPerson,
    BusinessOpportunity,
    Activity
)
admin.site.register(ContactPerson)
admin.site.register(Activity)
admin.site.register(BusinessOpportunity)



class ContactPersonAdmin(admin.ModelAdmin):
    pass

class BusinessOpportunityAdmin(admin.ModelAdmin):
    pass

class ActivityAdmin(admin.ModelAdmin):
    pass