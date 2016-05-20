from django.contrib import admin

from .models import TravelInfo


class TravelInfoAdmin(admin.ModelAdmin):
    list_display = [
        'leave_time',
        'return_time',
        'destination', 
        'reason'
        ]

admin.site.register(TravelInfo, TravelInfoAdmin)
