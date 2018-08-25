from django.dispatch import Signal

text_signal = Signal(providing_args=['line_id', 'text'])
postback_signal = Signal(providing_args=['line_id', 'postback_data'])