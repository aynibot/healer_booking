import requests
from django.core.cache import cache
from django.conf import settings
from linebot import LineBotApi

def get_bot_api():
    token = get_bot_token()
    return LineBotApi(token)

def get_bot_token():
    token = cache.get('bot_token', None)
    if token:
        return token

    url = 'https://api.line.me/v2/oauth/accessToken'
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    data = {}
    data['grant_type'] = 'client_credentials'
    data['client_id'] = settings.CHANNEL_ID
    data['client_secret'] = settings.CHANNEL_SECRET

    resp = requests.post(url, headers=headers, data=data)
    token = resp.json()['access_token']
    cache.set('bot_token', token, timeout=25*86400)
    return token

def push_templates(line_id, templates):
    line_bot_api = get_bot_api()
    line_bot_api.push_message(line_id, templates)

def multicast_templates(line_ids, templates):
    line_bot_api = get_bot_api()

    groups = [ line_ids[i:i+150] for i in range(0, len(line_ids), 150) ]
    for group in groups:
        line_bot_api.multicast(group, templates)