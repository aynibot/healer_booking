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
        greeting_text = '療癒師 {name} 您好！\n我是協助您為個案預約時段的機器人\n\n請透過下方選單操作預約喔！\n【預約個案】時段後( )內數字是剩餘名額，一時段最多2人\n【查詢時段】會顯示您已預約成功的記錄\n\n有任何疑問請洽工作人員，這裡無法提供解答喔\udbc0\udc8a'
        greeting_text = greeting_text.format(name=member.name)
        templates.append( TextSendMessage(text=greeting_text) )


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
