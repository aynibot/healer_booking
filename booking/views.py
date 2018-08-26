from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from .services import time_slot_service
# Create your views here.

class CronViewSet(ViewSet):

    @action(methods=['post'], detail=False, url_path='exec')
    def exec(self, request):
        time_slot_service.check_time_slot()

        return HttpResponse()