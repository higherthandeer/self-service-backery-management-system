from django.urls import re_path
from django.urls import path
from apps.system.consumers import YOLOv5Consumer, SaleConsumer
import re
from django.urls import path

websocket_urlpatterns = [
    # re_path(r"^room/(?P<group>\w+)", YOLOv5Consumer.as_asgi()),
    # re_path(r"ws/(?P<group>\w+)/$", YOLOv5Consumer.as_asgi()),
    path("api/yolov5/detect/", YOLOv5Consumer.as_asgi()),
    path("api/yolov5/sale/", SaleConsumer.as_asgi()),
]