import threading
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from .services import time_slot_service, reservation_service
from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Create your views here.

class CronViewSet(ViewSet):

    @action(methods=['post'], detail=False, url_path='exec')
    def exec(self, request):
        dt = datetime.now(tz=timezone('Asia/Taipei'))

        if dt.hour == 0 and dt.minute == 0:
            thrd = threading.Thread(target=time_slot_service.check_time_slot)
            thrd.start()

        elif dt.hour == 20 and dt.minute == 0:
            tomorrow = dt + relativedelta(days=1)
            kwargs = {'date_str':tomorrow.strftime('%Y-%m-%d')}
            thrd = threading.Thread(target=reservation_service.notify_healers, kwargs=kwargs)
            thrd.start()

        return HttpResponse()