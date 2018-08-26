from .repos import time_slot_repo
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

time_slot_service = TimeSlotService()