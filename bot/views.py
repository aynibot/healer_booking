from django.conf import settings
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from linebot import WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent, FollowEvent,
    TextSendMessage,TemplateSendMessage, ButtonsTemplate,
    URIAction, PostbackAction, MessageAction
)
from .utils import push_templates
from .signals import text_signal, postback_signal
from .services import member_service

handler = WebhookHandler(settings.CHANNEL_SECRET)

class LineBotViewSet(ViewSet):

    @action(methods=['post'], detail=False, url_path='webhook')
    def webhook(self, request):
        # get X-Line-Signature header value
        signature = request.META.get('HTTP_X_LINE_SIGNATURE')
        # get request body as text
        body = request.body.decode('utf-8')
        handler.handle(body, signature)

        return HttpResponse()

    @handler.add(FollowEvent)
    def handle_follow(event, *args, **kwargs):
        line_id = event.source.user_id
        reply_token = event.reply_token
        member = member_service.get_by_line_id(line_id)

        templates = []
        greeting_text = '療癒師 {name} 你好\n我是協助療癒師為個案預約時段的機器人\n電腦可以沒有人權但是蕭維玲必須有！\n各項功能都可以透過下方選單操作喔'
        greeting_text = greeting_text.format(name=member.name)
        templates.append( TextSendMessage(text=greeting_text) )

        actions = []
        actions.append( MessageAction(label='可預約時段查詢', text='#可預約時段查詢') )
        actions.append( MessageAction(label='我預約的時段', text='#我預約的時段') )
        btn = ButtonsTemplate(text='測試指令', actions=actions)
        templates.append(TemplateSendMessage(alt_text='測試指令', template=btn))

        push_templates( line_id, templates )

    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event, *args, **kwargs):
        line_id = event.source.user_id
        reply_token = event.reply_token
        text = event.message.text

        text_signal.send( sender=None, line_id=line_id, text=text )

    @handler.add(PostbackEvent)
    def handle_postback(event, *args, **kwargs):
        line_id = event.source.user_id
        reply_token = event.reply_token
        postback_data = event.postback.data

        postback_signal.send( sender=None, line_id=line_id, postback_data=postback_data )
