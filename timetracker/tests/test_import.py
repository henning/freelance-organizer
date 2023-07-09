import datetime
import os
from datetime import datetime, tzinfo

import pytest
from django.conf import settings

from timetracker.importer import TimeSliceImporter
from timetracker.models import TimeSlice, Project


class TestTimeSliceImporterTest:
    @pytest.mark.django_db
    def test_import_tsv_text(self):
        """
        Ensure importing a string in tab separated values format as timeslices.

        Prerequisites:
            * we have a multiline string with tsv data in format:
                STAR_DATE START_TIME END_DATE END_TIME DURATION DESCRIPTION
                wheer the separator is a tab, for example:
                2023-07-05	14:00	2023-07-05	17:10		03:10	Developing  someproject
                there can be invalid/empty lines - they will be ignored with a warning
        Expectation:
            * project name contained in the import data exists
            * after running the method with the string as parameter a timeslice
              is created for each valid line and saved with the additional properties
              is_imported=true and is_checked_after_import=false (so they can be reviewed manually)
        :return:
        """


        import_string="""
        Startdatum	Startzeit	Enddatum	Endzeit	Pause	net sum	Beschreibung	Projekt
        2023-07-05	14:00	2023-07-05	17:10		03:10	Developing	someproject
        2023-07-06	15:00	2023-07-06	19:10	10	04:00	Developing2	someproject
        					00:00	
        					04:00		someproject
        2023-07-07	13:00	2023-07-05	18:10		05:10	Developing3	someproject
        2023-07-07	13:00	2023-07-05	18:10		05:10	Developing4	someproject
        """

        Project(name="someproject").save()

        importer = TimeSliceImporter()

        importer.import_tsv_string(import_string)

        # ensure we have 3 new time slices and verify data for each of them
        timeslices = TimeSlice.objects.all()

        # TODO: no need to check the data, just check the call to import file...
        assert len(timeslices) == 4

        timeslice1 = TimeSlice.objects.get(description="Developing")

        assert timeslice1.is_imported

        # be sure to add the timezone...in db its utc
        assert timeslice1.start_time == datetime.fromisoformat("2023-07-05 14:00+02:00")
        assert timeslice1.end_time == datetime.fromisoformat("2023-07-05 17:10+02:00")
        assert timeslice1.break_duration_minutes == 0

        timeslice2 = TimeSlice.objects.get(description="Developing2")

        assert timeslice2.start_time == datetime.fromisoformat("2023-07-06 15:00+02:00")
        assert timeslice2.end_time == datetime.fromisoformat("2023-07-06 19:10+02:00")
        assert timeslice2.break_duration_minutes == 10

        timeslice3 = TimeSlice.objects.get(description="Developing3")

        assert timeslice3.start_time == datetime.fromisoformat("2023-07-07 13:00+02:00")
        assert timeslice3.end_time == datetime.fromisoformat("2023-07-05 18:10+02:00")
        assert timeslice3.break_duration_minutes == 0

    @pytest.mark.django_db
    def test_import_tsv_file_from_data_dir(self):
        """
        Ensure importing data from a TSV file that resides in the configured
        data directory works properly.

        prerequisites:

        * a tmp dir configured as datadir
        * a tsv file in the configured DATA dir

        expectation:
        * timeslices are imported.

        :return:
        """

        Project(name="someproject").save()

        settings.DATA_DIR=f"{os.path.dirname(__file__)}"

        importer = TimeSliceImporter()

        importer.import_tsv_file()

        assert len(TimeSlice.objects.all()) == 3

        timeslice1 = TimeSlice.objects.get(description="Developing")

        assert timeslice1.is_imported

        # be sure to add the timezone...in db its utc
        assert timeslice1.start_time == datetime.fromisoformat("2023-07-05 14:00+02:00")
        assert timeslice1.end_time == datetime.fromisoformat("2023-07-05 17:10+02:00")
        assert timeslice1.break_duration_minutes == 0

        timeslice2 = TimeSlice.objects.get(description="Developing2")

        assert timeslice2.start_time == datetime.fromisoformat("2023-07-06 15:00+02:00")
        assert timeslice2.end_time == datetime.fromisoformat("2023-07-06 19:10+02:00")
        assert timeslice2.break_duration_minutes == 10

        timeslice3 = TimeSlice.objects.get(description="Developing3")

        assert timeslice3.start_time == datetime.fromisoformat("2023-07-07 13:00+02:00")
        assert timeslice3.end_time == datetime.fromisoformat("2023-07-05 18:10+02:00")
        assert timeslice3.break_duration_minutes == 0
