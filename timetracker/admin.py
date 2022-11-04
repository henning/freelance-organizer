from calendar import monthrange
from datetime import date, timedelta
from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

import csv
from django.utils.timezone import localtime, get_current_timezone


from timetracker.models import (
    TimeSlice,
    Project
    )


class ProjectAdmin(admin.ModelAdmin):

    list_display = [
        'name']


class TimerangeListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Timerange')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'timerange'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('current_week', _('current week')),
            ('last_week', _('last week')),

            ('current_month', _('current month')),
            ('last_month', _('last month')),

            ('current_year', _('current year')),
            ('last_year', _('last year')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        today = date.today()
        year, week, weekday = today.isocalendar()

        if self.value() == 'current_week':
            # first day of this week
            first_day = today - timedelta(days=weekday-1)

            # last day of this week?
            last_day = first_day+timedelta(days=6)

        elif self.value() == 'last_week':
            first_day = today - timedelta(days=weekday+6)
            last_day = first_day + timedelta(days=6)

        elif self.value() == 'current_month':
            first_day = today - timedelta(days=today.day-1)
            month_days = monthrange(first_day.year, first_day.month)[1]
            last_day = first_day + timedelta(days=month_days-1)

        elif self.value() == 'last_month':
            last_day = today - timedelta(days=today.day)

            last_month_days = monthrange(
                last_day.year, last_day.month)[1]

            first_day = last_day - timedelta(days=last_month_days-1)

        elif self.value() == 'current_year':
            first_day = date(day=1, month=1, year=today.year)
            last_day = date(day=31, month=12, year=today.year)
        elif self.value() == 'last_year':
            first_day = date(day=1, month=1, year=today.year-1)
            last_day = date(day=31, month=12, year=today.year-1)
        else:
            return queryset

        print(first_day)
        print(last_day+timedelta(days=1))

        return queryset.filter(start_time__gte=first_day,
                               start_time__lte=last_day+timedelta(days=1))


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
        TimerangeListFilter,
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
        project_hour_summaries = dict()

        for timeslice in qs:
            project = timeslice.project
            duration_summary += timeslice.duration_minutes()

            if project not in project_hour_summaries.keys():
                project_hour_summaries[project] = 0

            project_hour_summaries[project] += timeslice.duration_minutes()

        for project in project_hour_summaries.keys():
            project_hour_summaries[project] = round(project_hour_summaries[project]/60, 2)

        response.context_data['project_hour_summaries'] = project_hour_summaries
        response.context_data['duration_summary_hours'] = round(duration_summary/60, 2)
        response.context_data['duration_summary_days'] = round(duration_summary/60/8, 2)

        return response

    actions = [toggle_invoiced, export]


admin.site.register(TimeSlice, TimeSliceAdmin)
admin.site.register(Project, ProjectAdmin)
