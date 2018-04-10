from django.contrib import admin
from django.http import HttpResponse
import csv
from django.utils.timezone import localtime, get_current_timezone


from timetracker.models import (
    TimeSlice,
    Project
    )


class ProjectAdmin(admin.ModelAdmin):

    list_display = [
        'name']

 
class TimeSliceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.filter(project__is_active=True)

    def toggle_invoiced(self, request, queryset):
        for timeslice in queryset:
            if timeslice.is_invoiced is True:
                timeslice.is_invoiced = False
            elif timeslice.is_invoiced is False:
                timeslice.is_invoiced = True
            
            timeslice.save()

    toggle_invoiced.short_description='toggle invoiced state'

    def export(self, request, queryset):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="zeiten.csv"'
    
        writer = csv.writer(response)
    
        duration_sum = 0
               
        writer.writerow([
            'Beginn', 
            'Ende', 
            'Pause',
            'Dauer',
            'Beschreibung',
            'Projekt',
            'Abgerechnet'
        ])
         
        for time_slice in queryset:
            duration_sum += time_slice.duration_minutes()

            if time_slice.project is not None:
                project_name = time_slice.project.name.encode('utf-8')
            else:
                project_name = ''
                
            writer.writerow([
                localtime(
                    time_slice.start_time,
                    get_current_timezone()).strftime('%Y-%m-%d %H:%M'),
                localtime(
                    time_slice.end_time,
                    get_current_timezone()).strftime('%Y-%m-%d %H:%M'),
                str(time_slice.break_duration_minutes),
                str(time_slice.duration_minutes()),
                time_slice.description,
                project_name,
                str(time_slice.is_invoiced)
                ])
        
        writer.writerow([
            '', 
            '',
            '',
            duration_sum/60,
            ])

        return response

    fields = [
        'start_time',
        'end_time',
        'description',
        'break_duration_minutes', 
        'project', 
        'is_invoiced']
    
    search_fields = ['description', 'project__name']

    list_display = [
        'start_time',
        'end_time',
        'project',
        'description',
        'duration_minutes',
        'break_duration_minutes', 
        'is_invoiced']
    
    list_filter = (
        ('project',admin.RelatedOnlyFieldListFilter),
        'is_invoiced',
        'start_time',
        )

    # only let us select active projects
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.filter(is_active=True)

        formfield = super(TimeSliceAdmin, self).formfield_for_foreignkey(
            db_field,
            request,
            **kwargs)

        return formfield

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):

            return response

        duration_summary = 0

        for timeslice in qs:
            duration_summary += timeslice.duration_minutes()

        response.context_data['duration_summary_hours'] = round(duration_summary/60, 2)
        response.context_data['duration_summary_days'] = round(duration_summary/60/8, 2)

        return response

    actions = [toggle_invoiced, export]


admin.site.register(TimeSlice, TimeSliceAdmin)
admin.site.register(Project, ProjectAdmin)
