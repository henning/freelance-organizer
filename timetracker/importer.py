import csv
from io import StringIO, open

import django.db.transaction
from django.conf import settings
import os

from django.core.exceptions import ValidationError
from django.db import transaction

from timetracker.models import TimeSlice, Project


class TimeSliceImporter():
    def import_tsv_string(self, import_string):
        # read the tsv string into a csv object
        import_string_io = StringIO(import_string)
        return self.import_tsv_file(import_string_io)

    def import_tsv_file(self, import_file=None):

        if import_file is None:
            import_file_name = f"{settings.DATA_DIR}{os.path.sep}import.tsv"
            import_file = open(import_file_name)

        data_reader = csv.reader(import_file, delimiter="\t")
        # create timeslices for each row
        import_count=0
        row_count = 0

        for row in data_reader:
            print(row)
            row_count+=1

            rowlen = len(row)
            if rowlen < 8:
                print(f"Line incomplete - {rowlen} is too short: {row}")
                continue

            slice = TimeSlice()

            # cells that must not be empty

            slice.start_time = f"{row[0].strip()} {row[1]}"
            if slice.start_time.strip()=="":
                print(f"empty start time in row {row}")
                continue
            slice.end_time = f"{row[2]} {row[3]}"

            if slice.end_time.strip() == "":
                print(f"empty start time in row {row}")
                continue

            break_minutes = row[4]
            if len(break_minutes) == 0:
                slice.break_duration_minutes = 0
            else:
                try:
                    slice.break_duration_minutes = int(break_minutes)
                except ValueError:
                    print(f"Cannot parse break minutes. Incorrect line: {row}")
                    continue
            # sum is 5 but we calculate it ourselves
            slice.description = row[6]
            try:
                project_name = row[7]
            except IndexError:
                print(f"Line too short.")
                continue
            try:
                slice.project = Project.objects.get(name=project_name)
            except Project.DoesNotExist:
                print(f"Project {project_name} does not exist. skipping")
                continue

            slice.is_imported=True
            slice.save()
            # except ValidationError as e:
            #     print(e)
            #     print(f"Validation error on saving row: {row}")
            #     #django.db.transaction.rollback()
            #     continue

            import_count+=1

        import_file.close()
        print(f"imported {import_count} of {row_count} rows")
