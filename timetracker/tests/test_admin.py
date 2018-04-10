from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from timetracker.models import TimeSlice, Project
from timetracker.admin import TimeSliceAdmin


class MockSuperUser(object):

    def has_perm(self, perm):
        return True

    def is_active(self):
        return True

    is_staff = True


class TestTimeSliceAdmin(TestCase):

    def test_export(self):

        # create a few timeslices with start / stop times and durations
        test_slice = TimeSlice(start_time='2014-01-01 08:15+01:00',
                          end_time='2014-01-01 11:47+01:00')
        test_slice.break_duration_minutes = 15

        test_slice.save()

        site = AdminSite()
        admin = TimeSliceAdmin(TimeSlice, site)

        request_factory = RequestFactory()
        request = request_factory.get('/path', data={'name': u'test'})
        queryset = TimeSlice.objects.all()

        export = str(admin.export(request, queryset).content)

        assert "08:15" in export

        # Ensure no timezone stuff in the datetimes...

        assert "+00:00" not in export
        assert "+01:00" not in export
        assert "+02:00" not in export
        assert "+" not in export

        assert ",3" in export

    def test_inactive_projects_not_selectable_for_timeslice_creation(self):
        """
        Given we have created 5 projects and made 3 inactive

        When we start to create a new timeslice

        We only want active projects in the selection
        """

        for i in range(1,6):
            project = Project(
                name='project{}'.format(str(i)),
                description='project {}'.format(str(i)))

            if i % 2 == 0:
                project.is_active = False

            project.save()

        site = AdminSite()

        admin = TimeSliceAdmin(TimeSlice, site)

        request_factory = RequestFactory()
        add_path = reverse('admin:timetracker_timeslice_add')
        request = request_factory.get(add_path)
        request.user = MockSuperUser()

        form = admin.get_form(request)()

        formstring = str(form)

        assert u'project1' in formstring
        assert 'project2' not in formstring
        assert 'project3' in formstring
        assert 'project4' not in formstring
        assert 'project5' in formstring
