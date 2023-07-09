import csv
from io import StringIO

from django.core.exceptions import ObjectDoesNotExist

from timetracker.models import TimeSlice, Project


class TimeSliceImporter():
    def import_tsv_string(self, import_string):
        # read the tsv string into a csv object
        import_string_io = StringIO(import_string)
        data_reader = csv.reader(import_string_io, delimiter="\t")
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

            slice.start_time = f"{row[0].strip()} {row[1]}"
            slice.end_time = f"{row[2]} {row[3]}"

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
            import_count+=1

        print(f"imported {import_count} of {row_count} rows")
