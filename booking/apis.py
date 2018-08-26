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
        while len(group) >= 3:
            group.append(None)

        actions = []
        for slot in group:
            if slot:
                label = slot.date
                data = 'DATE#{}'.format(slot.date)
                actions.append( PostbackAction(label=label, data=build_postback_data(data)) )
            else:
                actions.append( PostbackAction(label=' ', data='') )

        cols.append( CarouselColumn(text='請選擇想預約的日期', actions=actions) )

    templates = TemplateSendMessage(alt_text='開放預約日期', template=CarouselTemplate(columns=cols))
    push_templates(line_id, templates)

def build_postback_data(data):
    postback_data = '{prefix}_{data}'.format(prefix=PREFIX, data=data.upper())
    return postback_data