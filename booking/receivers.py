from bot.signals import text_signal, postback_signal

def recieve_text(line_id, text, **kwargs):
    if text == '#可預約時段查詢':
        pass
    elif text == '#我預約的時段':
        pass

def receive_postback(line_id, postback_data, **kwargs):

    if not postback_data.startswith('BOOK'):
        return



text_signal.connect( recieve_text )
postback_signal.connect( receive_postback )