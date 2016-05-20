# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 19:23
from __future__ import unicode_literals

from django.db import migrations, models


def set_existing_projects_inactive(apps, schema_editor):
    """
    we have a default True for new projects, but the *currently*
    existing projects in production are mostly old,
    so set them inactive, and activate as needed.
    """
    Project = apps.get_model('timetracker', 'Project')

    for project in Project.objects.all():
        project.is_active = False
        project.save()

class Migration(migrations.Migration):

    dependencies = [
        ('timetracker', '0002_auto_20160331_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(set_existing_projects_inactive)
    ]
