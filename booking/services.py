from bot.services import member_service
from .repos import time_slot_repo, reservation_repo
from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TimeSlotService(object):
    def check_time_slot(self):
        time_slot_repo.check_time_slot()

    def get_booking_days(self):
        tz = timezone('Asia/Taipei')
        now = datetime.now(tz=tz)

        start_dt = now + relativedelta(days=1)
        start_dt = start_dt.strftime('%Y-%m-%d')

        end_dt = now + relativedelta(days=15)
        end_dt = end_dt.strftime('%Y-%m-%d')

        return time_slot_repo.get_booking_days(start_dt, end_dt)

    def get_booking_slots(self, date_str):
        return time_slot_repo.get_booking_slots(date_str)

    def get_slot_by_id(self, slot_id):
        return time_slot_repo.get_by_id(slot_id)

class ReservationService(object):
    def check_slot_available(self, time_slot):
        count = reservation_repo.get_slot_counts(time_slot.id)
        if time_slot.max_amount <= count:
            return False

        return True

    def create(self, line_id, time_slot):
        member = member_service.get_by_line_id(line_id)
        customer_name = '{name} 的個案'.format(name=member.name)
        return reservation_repo.create(member.id, time_slot.id, customer_name)

    def get_latest(self, line_id):
        member = member_service.get_by_line_id(line_id)
        return reservation_repo.get_by_member_id(member.id).order_by('-id').first()

time_slot_service = TimeSlotService()
reservation_service = ReservationService()