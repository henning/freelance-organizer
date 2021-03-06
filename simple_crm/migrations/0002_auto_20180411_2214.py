# Generated by Django 2.0.4 on 2018-04-11 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simple_crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='business_opportunity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='simple_crm.BusinessOpportunity'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='contact_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='simple_crm.ContactPerson'),
        ),
        migrations.AlterField(
            model_name='businessopportunity',
            name='contact_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='simple_crm.ContactPerson'),
        ),
    ]
