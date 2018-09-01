from pytz import timezone
from datetime import datetime
from .services import time_slot_service, reservation_service
from bot.utils import push_templates

from linebot.models import (
    TemplateSendMessage, CarouselTemplate, CarouselColumn, PostbackAction, TextSendMessage,
)

WEEKDAY = ('星期一','星期二','星期三','星期四','星期五','星期六','星期天',)
PREFIX = 'BOOK'
def build_postback_data(data):
    postback_data = '{prefix}_{data}'.format(prefix=PREFIX, data=data.upper())
    return postback_data

def push_booking_days(line_id):
    slots = time_slot_service.get_booking_days()
    cols = []
    groups = [ slots[i:i+3] for i in range( 0,len(slots),3 ) ]
    for group in groups:
        while len(group) < 3:
            group.append(None)

        actions = []
        for slot in group:
            if slot:
                year, month, day = slot.date.split('-')
                dt = datetime.strptime(slot.date, '%Y-%m-%d').replace(tzinfo=timezone('Asia/Taipei'))
                label = '{month}-{day} {weekday}'.format(month=month, day=day, weekday=WEEKDAY[dt.weekday()])
                data = 'DATE#{}'.format(slot.date)
                actions.append( PostbackAction(label=label, data=build_postback_data(data)) )
            else:
                actions.append( PostbackAction(label=' ', data=' ') )

        cols.append( CarouselColumn(text='請選擇想預約的日期', actions=actions) )

    templates = TemplateSendMessage(alt_text='開放預約日期', template=CarouselTemplate(columns=cols))
    push_templates(line_id, templates)

def push_booking_slot(line_id, date_str):
    booking_info = time_slot_service.get_booking_slots(date_str)

    cols = []
    groups = [booking_info[i:i + 3] for i in range(0, len(booking_info), 3)]
    for group in groups:
        while len(group) < 3:
            group.append(None)

        carousel_text = '預約的日期是{date}，請選擇時段'
        actions = []
        for info in group:
            if info:
                carousel_text = carousel_text.format(date=info['slot'].date)
                begin = info['slot'].hour
                end = begin+1
                label = '{begin}點-{end}點 ({remain})'.format(begin=begin, end=end, remain=info['remain'])
                data = 'CONFIRM#{}'.format(info['slot'].id)
                actions.append( PostbackAction(label=label, data=build_postback_data(data)) )
            else:
                actions.append( PostbackAction(label=' ', data=' ') )

        cols.append( CarouselColumn(text=carousel_text, actions=actions) )

    templates = TemplateSendMessage(alt_text='請選擇預約的時段', template=CarouselTemplate(columns=cols))
    push_templates(line_id, templates)

def push_booking_confirm(line_id, slot_id):
    time_slot = time_slot_service.get_slot_by_id(slot_id)
    if not reservation_service.check_slot_available(time_slot):
        return push_templates(line_id, TextSendMessage(text='阿阿！\n你想預約的時段已經滿了，可以選擇其他的時段嗎？'))

    # TODO check time table
    reservation_service.create(line_id, time_slot)
    push_templates(line_id, TextSendMessage(text='預約成功囉！請問我們要怎麼稱呼你的個案呢？'))

def push_my_reservation(line_id):
    tz = timezone('Asia/Taipei')
    today = datetime.now(tz=tz).strftime('%Y-%m-%d')
    reservations = reservation_service.get_by_line_id(line_id).filter(time_slot__date__gte=today).order_by('time_slot__date')[:10]

    if len(reservations) <= 0:
        push_templates(line_id, TextSendMessage(text='你目前沒有預約任何時段喔！'))
        return

    cols = []
    for reservation in reservations:
        info = {}
        info['customer'] = reservation.customer_name
        info['date'] = reservation.time_slot.date
        info['begin'] = reservation.time_slot.hour
        info['end'] = reservation.time_slot.hour+1

        text = '{customer}\n{date}\n{begin}:00 ~ {end}:00'.format(**info)
        data = 'CANCEL#{id}'.format(id=reservation.id)
        actions = [PostbackAction(label='取消預約', data=build_postback_data(data))]
        cols.append( CarouselColumn(text=text, actions=actions) )

    templates = TemplateSendMessage(alt_text='預約時段查詢', template=CarouselTemplate(columns=cols))
    push_templates(line_id, templates)

def cancel_booking(line_id, reservation_id):
    reservation = reservation_service.get_reservation_by_id(reservation_id)
    if reservation:
        reservation.delete()

    push_my_reservation(line_id)
    return reservation