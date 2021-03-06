from linebot.models import TextSendMessage

from bot.signals import text_signal, postback_signal
from bot.utils import push_templates, multicast_templates
from .apis import (
    push_booking_days, push_booking_slot, push_booking_confirm, push_my_reservation,
    cancel_booking,
)

from .services import reservation_service

def recieve_text(line_id, text, **kwargs):
    if text == '#可預約時段查詢':
        push_booking_days(line_id)

    elif text == '#我預約的時段':
        push_my_reservation(line_id)

    # TODO 問答事件table
    reservation = reservation_service.get_latest(line_id)
    if reservation and reservation.customer_name.endswith('的個案'):
        reservation.customer_name = text
        reservation.save()
        push_templates(line_id, TextSendMessage(text='完成囉！我們到時見^_^~'))

        from bot.services import member_service
        admins = member_service.get_admins()
        admin_line_ids = [member.line_id for member in admins]
        text = '新增了一筆預約\n\n{reservation}'.format(reservation=reservation)
        multicast_templates(admin_line_ids, TextSendMessage(text=text))
        return

def receive_postback(line_id, postback_data, **kwargs):
    if not postback_data.startswith('BOOK'):
        return

    type, *args = postback_data.replace('BOOK_', '').split('#')
    if type == 'DATE':
        push_booking_slot(line_id, *args)

    elif type == 'CONFIRM':
        push_booking_confirm(line_id, *args)

    elif type == 'CANCEL':
        reservation = cancel_booking(line_id, *args)
        if reservation:
            from bot.services import member_service
            admins = member_service.get_admins()
            admin_line_ids = [member.line_id for member in admins]
            text = '取消了一筆預約\n\n{reservation}'.format(reservation=reservation)
            multicast_templates(admin_line_ids, TextSendMessage(text=text))

text_signal.connect( recieve_text )
postback_signal.connect( receive_postback )