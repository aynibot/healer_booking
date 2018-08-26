from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
# Create your views here.

class CronViewSet(ViewSet):

    @action(methods=['post'], detail=False, url_path='exec')
    def exec(self, request):


        return HttpResponse()