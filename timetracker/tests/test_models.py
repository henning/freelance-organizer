import pytest
from django.test import TestCase

from timetracker.models import TimeSlice, Project


class TestTimeTracker(TestCase):

    def test_duration_calculation(self):
        """
        Check if duration calculation works for a timeslice.
        """

        slice = TimeSlice(start_time='2014-01-01 08:15+00:00',
                          end_time='2014-01-01 11:47+00:00')
        slice.save()

        slice = TimeSlice.objects.get(pk=slice.id)

        self.assertEquals(212, slice.duration_minutes())

        slice.break_duration_minutes = 15

        self.assertEquals(197, slice.duration_minutes())


class TestProjects:

    @pytest.mark.django_db
    def test_order_by_name(self):
        project1 = Project(name='c')
        project1.save()

        project2 = Project(name='a')
        project2.save()

        project3 = Project(name='b')
        project3.save()

        all_projects = Project.objects.all()

        assert list(all_projects) == [ project2, project3, project1]
