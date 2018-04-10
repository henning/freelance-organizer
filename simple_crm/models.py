from django.db import models

"""
Simple CRM.
This simple CRM is about to track activities that have been done
or need to be done in the future to create a business relation leading to a
contracting with an customer, or help mainatining an existing contract for a
running project.
"""

class BaseModel(models.Model):
    """
    Some generic properties that we want to have in all our Objects.
    """

    created = models.DateTimeField(auto_now_add=True)

    last_changed = models.DateTimeField(auto_now=True)

    notes = models.TextField(blank=True)


class ContactPerson(BaseModel):
    """
    Represents a person to which we have a and maintain a contact in order
    to realize a possible business opportunity or maintain an existing one.
    """

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    company_name = models.CharField(max_length=80, blank=True)

    xing_url = models.URLField(max_length=80, blank=True)
    web_url = models.URLField(blank=True)
    phone = models.CharField(blank=True, max_length=42)
    skype_name = models.CharField(max_length=42, blank=True)

    class Meta:
        ordering = ["last_name", "first_name", "company_name"]

    def __str__(self):
        if self.company_name is not None:
            return '{} {} - {}'.format(
                self.last_name, self.first_name, self.company_name)
        else:
            return '{} {}'.format(self.last_name, self.first_name)


class BusinessOpportunity(BaseModel):
    """
    A business opportunity is a possibility to create a contract for a project
    to be handled to fulfill a customer's needs.
    """

    name = models.CharField(max_length=80)

    description = models.TextField(blank=True)

    is_open = models.BooleanField(default=True)
    is_realized = models.BooleanField(default=False)

    contact_person = models.ForeignKey(
        ContactPerson, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ["name", "last_changed"]

    def __str__(self):
        return self.name


class Activity(BaseModel):
    """
    An activity related to a business opportunity or a contact person
    that might lead to realizing or creating a business opportunity.
    """

    short_description = models.CharField(max_length=80)

    contact_person = models.ForeignKey(
        ContactPerson, blank=True, null=True, on_delete=models.PROTECT)

    business_opportunity = models.ForeignKey(
        BusinessOpportunity, blank=True, null=True, on_delete=models.PROTECT)

    # date_due
    # date_start
    # date_completed

    def __str__(self):
        return self.short_description

