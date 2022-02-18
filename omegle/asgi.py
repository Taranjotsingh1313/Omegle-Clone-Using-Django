"""
ASGI config for omegle project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from App.consumers import ChatConsumer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omegle.settings')

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter(
            [
            path('chat/',ChatConsumer.as_asgi())
            ]
        )
        )
    )
})