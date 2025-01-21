from django.urls import path
from .consumers import FlagConsumer

websocket_urlpatterns = [
    path('ws/flags/', FlagConsumer.as_asgi()),
]