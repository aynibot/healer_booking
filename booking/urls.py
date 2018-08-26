from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import CronViewSet

router = DefaultRouter()

router.register(r'cron', CronViewSet, base_name='cron')

urlpatterns = [
	url(r'^api/', include(router.urls)),
]

