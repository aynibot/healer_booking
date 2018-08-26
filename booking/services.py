from linebot.models import TextSendMessage
from bot.services import member_service
from bot.utils import multicast_templates
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

    def get_by_line_id(self, line_id):
        member = member_service.get_by_line_id(line_id)
        return reservation_repo.get_by_member_id(member.id)

    def get_reservation_by_id(self, id):
        return reservation_repo.get_by_id(id)

    def notify_healers(self, date_str):
        # send to healer
        reservations = reservation_repo.get_by_date(date_str)

        member_ids = reservations.values_list('member_id', flat=True)
        members = member_service.get_by_member_ids(member_ids)
        healers_line_ids = members.values_list('line_id', flat=True)
        multicast_templates(healers_line_ids, TextSendMessage('別忘了關心個案喔！\n我們明天見^_^~'))

        # send to admin
        member_info = { member.id:member for member in members }
        report = {}
        admin_line_ids = member_service.get_admins().values_list('line_id', flat=True)
        for reservation in reservations:
            hour = reservation.time_slot.hour
            if hour not in report:
                report[hour] = []

            healer = member_info[reservation.member_id]
            report[hour].append( '    {healer} 的個案 {customer}'.format(healer=healer.name, customer=reservation.customer_name) )

        report_text = ''
        for begin, info in report.items():
            text = '{begin}:00 ~ {end}:00\n'.format(begin=begin, end=begin+1)
            text += '\n'.join(info)
            report_text += (text + '\n')

        multicast_templates(admin_line_ids, TextSendMessage(report_text))

time_slot_service = TimeSlotService()
reservation_service = ReservationService()