from .services import time_slot_service
from bot.utils import push_templates

from linebot.models import (
    TemplateSendMessage, CarouselTemplate, CarouselColumn, PostbackAction
)

PREFIX = 'BOOK'

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
                label = slot.date
                data = 'DATE#{}'.format(slot.date)
                actions.append( PostbackAction(label=label, data=build_postback_data(data)) )
            else:
                actions.append( PostbackAction(label=' ', data=' ') )

        cols.append( CarouselColumn(text='請選擇想預約的日期', actions=actions) )

    templates = TemplateSendMessage(alt_text='開放預約日期', template=CarouselTemplate(columns=cols))
    push_templates(line_id, templates)

def build_postback_data(data):
    postback_data = '{prefix}_{data}'.format(prefix=PREFIX, data=data.upper())
    return postback_data

def push_booking_slot(line_id, date_str):
    booking_info = time_slot_service.get_booking_slots(date_str)

    cols = []
    groups = [booking_info[i:i + 3] for i in range(0, len(booking_info), 3)]
    for group in groups:
        while len(group) < 3:
            group.append(None)

        actions = []
        for info in group:
            if info:
                begin = info['slot'].hour
                end = begin+1
                label = '{begin}點-{end}點 ({remain})'.format(begin=begin, end=end, remain=info['remain'])
                data = 'CONFIRM#{}'.format(info['slot'].id)
                actions.append( PostbackAction(label=label, data=build_postback_data(data)) )
            else:
                actions.append( PostbackAction(label=' ', data=' ') )

        cols.append( CarouselColumn(text='預約的日期是{date}，請選擇時段'.format(date=info['slot'].date), actions=actions) )

    templates = TemplateSendMessage(alt_text='請選擇預約的時段', template=CarouselTemplate(columns=cols))
    push_templates(line_id, templates)

def push_booking_confirm(line_id, slot_id):
    pass