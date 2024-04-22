from django.db import models
from django.db.models import TextField, BooleanField


class Project(models.Model):
    """
    A project we're working on - either for ourselves or others, 
    by which we want to be able to filter/sort TimeSlices for overview and
    progress/cost control as well as for invoicing.
    """
    
    name = models.CharField(max_length=140)
    
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TimeSlice(models.Model):
    """
    A timeslice represents a timeframe worked on something.
    """

    start_time = models.DateTimeField('start time', null=True, blank=True)

    end_time = models.DateTimeField('end_time', null=True, blank=True)

    description = models.CharField(max_length=1024)

    # duration of an eventual break - sometimes you know you didn't work the
    # full time on this thing, but you made a break in between but cannot
    # determine exactly the time so splitting
    # into multiple slices doesn't make much sense.
    break_duration_minutes = models.IntegerField(default=0)

    project = models.ForeignKey(Project, null=True, on_delete=models.PROTECT)
    
    is_invoiced = models.BooleanField(default=False)

    is_imported = models.BooleanField(default=False)

    is_checked_after_import = models.BooleanField(default=False)
   
    def duration_minutes(self):
        """
        Return this slice's duration in minutes.
        """

        if self.end_time is None or self.start_time is None:
            return 0
        
        duration_delta = self.end_time - self.start_time

        duration_minutes = duration_delta.seconds/60

        if self.break_duration_minutes is not None:
            duration_minutes = duration_minutes - float(self.break_duration_minutes)

        return round(duration_minutes,2)

    def __str__(self):
        return self.description


class ImportData(models.Model):

    creation_timestamp = models.DateTimeField(auto_now=True, editable=False)

    # TODO: Should this be editable?
    # if changed, we must delete data imported by this and run import process again...
    # so maybe better to not allow editing
    import_data = TextField(blank=False, null=False)

    import_done = BooleanField(default=False)

    notes = TextField(blank=True, null=True)

    # TODO: Relation to the TimeSlices created based on this data

    # TODO: Timestamp when the import has been done? here or in the TimeSlice?
    #  maybe this here should have an import_run datetime... while timeSLices
    #  still could have an creation timestamp?
    # maybe we even want import started and import finished date to have
    # information when an import did not finish properly


    # TODO: import_run_results? errors, messages and number of
    #  timeslices created or so? (because the relation will only show slices
    #  that still exist...

    # TODO: how to treat re-imports, e.g. because the importer code has been
    #  changed/improved/fixed?
    # -> maybe thats not a standard behaviour, but if such cases become
    #    necessary we must individually decide what's best to do (e.g. delete
    #    all Timeslices based on an import, reimport, set date etc again?)
