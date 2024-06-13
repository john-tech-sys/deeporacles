

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# import chat.routing
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator


application = ProtocolTypeRouter({
    # No need for WebSocket routing, so remove the "websocket" key
})

# application = ProtocolTypeRouter({
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })
# from django.urls import path, re_path

# from chat.private_consumers import ChatConsumer
# from chat.forum_consumers import ForumChatConsumer
# from contrib.consumers import NotificationConsumer


# application = ProtocolTypeRouter({
# 	'websocket': AllowedHostsOriginValidator(
# 		AuthMiddlewareStack(
# 			URLRouter([
# 					path('', NotificationConsumer),
# 					path('chat/<room_id>/', ChatConsumer),
# 					path('public_chat/<room_id>/', ForumChatConsumer),
# 			])
# 		)
# 	),
# })