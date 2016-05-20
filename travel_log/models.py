from django.db import models


class TravelInfo(models.Model):
    """
    Information on a travel taken for business reasons.
    Can be of general interest and statistics, but also to be used for
    calculating tax relevant data - in Germany for example out of
    house working time results in specific amounts that can be calculated
    as business expenses.
    """
    leave_time = models.DateTimeField()

    return_time = models.DateTimeField(blank=True, null=True)

    destination = models.CharField(max_length=140)

    reason = models.CharField(max_length=256)

    notes = models.TextField(blank=True, null=True)

    # if theres private stuff done in between, we substract these times.
    free_days = models.IntegerField(default=0)

    # if the hotel stay costs already include a breakfast, we can apply
    # only a smaller value for the travel.
    hotel_stay_with_breakfast = models.BooleanField(default=False)


# These shall be calculated(cusom Manager?!)
# * Stunden erster Tag
# * volle Tage
# * Stunden letzter Tag
