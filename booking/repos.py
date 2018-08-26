from django.db.models import Count
from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import TimeSlot, DefaultTimeSlot, Reservation


class TimeSlotRepo(object):

    def check_time_slot(self):
        tz = timezone('Asia/Taipei')
        now = datetime.now(tz=tz)

        default_slot_info = {}
        for row in DefaultTimeSlot.objects.all():
            weekday = row.weekday
            if weekday not in default_slot_info:
                default_slot_info[weekday] = []

            default_slot_info[weekday].append(row)

        time_slots = TimeSlot.objects.order_by('-date').distinct('date').values_list('date', flat=True)[:30]
        time_slots = set(time_slots)

        new_rows = []
        for shift_days in range(15):
            dt = now + relativedelta(days=shift_days)
            date_str = dt.strftime('%Y-%m-%d')
            if date_str in time_slots:
                continue

            weekday = dt.weekday()
            default_slots = default_slot_info.get(weekday, [])
            for default_slot in default_slots:
                hour = default_slot.hour
                max_amount = default_slot.max_amount
                new_rows.append( TimeSlot(date=date_str, hour=hour, max_amount=max_amount) )

        TimeSlot.objects.bulk_create(new_rows)

    def get_booking_days(self, start_dt, end_dt):
        return TimeSlot.objects.filter(date__range=(start_dt, end_dt,)).distinct('date').order_by('date')

    def get_booking_slots(self, date_str):
        time_slots = TimeSlot.objects.filter(date=date_str).order_by('hour')
        time_slot_ids = [ slot.id for slot in time_slots ]
        rows = Reservation.objects.filter(time_slot_id__in=time_slot_ids).values('time_slot_id').annotate(count=Count('time_slot_id'))
        reservation_info = { row['time_slot_id']:row['count'] for row in rows }

        result = []
        for slot in time_slots:
            remain_count = slot.max_amount - reservation_info.get(slot.id, 0)
            if remain_count <= 0:
                continue

            info = {}
            info['slot'] = slot
            info['remain'] = remain_count
            result.append(info)

        return result

class ReservationRepo(object):
    def create(self, member_id, time_slot_id):
        return Reservation.objects.create(member_id=member_id, time_slot_id=time_slot_id)

    def get_by_id(self, id):
        return Reservation.objects.get(id=id)

    def get_by_member_id(self, member_id):
        return Reservation.objects.filter(member_id=member_id)

    def get_by_date(self, date_str):
        time_slot_ids = TimeSlot.objects.filter( date=date_str ).values_list('id', flat=True)
        return Reservation.objects.filter( time_slot_id__in=time_slot_ids )

time_slot_repo = TimeSlotRepo()
reservation_repo = ReservationRepo()