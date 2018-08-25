from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


from .views import LineBotViewSet

router = DefaultRouter()

router.register(r'line', LineBotViewSet, base_name='line')

urlpatterns = [
	url(r'^api/', include(router.urls)),
]

