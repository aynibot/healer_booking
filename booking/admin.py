from django.contrib import admin

from .models import DefaultTimeSlot
from .models import TimeSlot
from .models import Reservation

# Register your models here.
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('member', 'customer_name', 'time_slot', )
    list_filter = ('member', 'time_slot__date',)

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'hour',)
    list_filter = ('date',)

admin.site.register(DefaultTimeSlot)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(Reservation, ReservationAdmin)