from django.db import models
from .constans import WEEKDAY

from bot.models import Member

class Basis(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
class DefaultTimeSlot(models.Model):
    weekday = models.PositiveIntegerField(choices=WEEKDAY)
    hour = models.PositiveIntegerField()
    max_amount = models.PositiveIntegerField(default=2)

class TimeSlot(models.Model):
    date = models.CharField(max_length=16)
    hour = models.PositiveIntegerField()
    max_amount = models.PositiveIntegerField(default=2)

    def __str__(self):
        hour = self.hour
        return '{date} {hr_begin}點-{hr_end}點'.format( date=self.date, hr_begin=hour, hr_end=(hour+1) )

class Reservation(Basis):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    customer_name = models.CharField( max_length=128, default=None, null=True, blank=True )

    def __str__(self):
        return '{healer} 預約 {customer} 在 {time}'.format( healer=self.member, customer=self.customer_name, time=self.time_slot )
