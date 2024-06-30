# from rest_framework.viewsets import ModelViewSet
# import subprocess
# import os
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.views import APIView
# from rest_framework import status
#
#
# class YoloV5DetectView(APIView):
#     """登录视图"""
#     authentication_classes = []
#     permission_classes = []
#
#     def post(self, request):
#         if 'file' in request.FILES:
#             print(1)
#             uploaded_file = request.FILES['file']
#             file_name = uploaded_file.name
#
#             # 构建文件保存路径，假设您将文件保存在 media 目录下
#             file_path = os.path.join('media', file_name)
#
#             # 保存文件
#             with open(file_path, 'wb') as f:
#                 for chunk in uploaded_file.chunks():
#                     f.write(chunk)
#             p = subprocess.Popen('python D:\yolov5-master\detect.py ' + "--source 0",
#                                  stdin=subprocess.PIPE,
#                                  stdout=subprocess.PIPE)
#             out = p.stdout.readlines()
#             print(out)
#             return Response({'filePath': file_path, 'fileName': file_name})
#         else:
#             print(2)
#             return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)


import subprocess
import cv2
import numpy as np
import asyncio
import websockets
from django.http import HttpResponse
from rest_framework.views import APIView


class YOLOv5DetectView(APIView):
    async def detect_objects(self, websocket):
        process = subprocess.Popen(['python', 'D:\yolov5-master\detect.py', '--source', '0'],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            # 从 YOLOv5 获取检测结果
            detection_result = process.stdout.readline().decode().strip()
            if not detection_result:
                break
            # 在视频帧上绘制检测框
            frame = np.zeros((480, 640, 3), dtype=np.uint8)  # 创建一个空白视频帧
            # 解析检测结果，并在视频帧上绘制检测框
            # 这里需要根据具体的检测结果格式和绘制方法进行相应的实现
            # 示例代码假设检测结果格式为："<class_name> <x_center> <y_center> <width> <height>"
            class_name, x_center, y_center, width, height = detection_result.split()
            x1 = int(float(x_center) - float(width) / 2)
            y1 = int(float(y_center) - float(height) / 2)
            x2 = int(float(x_center) + float(width) / 2)
            y2 = int(float(y_center) + float(height) / 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 绘制检测框
            # 将带有检测框的视频帧转换为二进制数据
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            # 发送带有检测框的视频帧给前端
            await websocket.send(frame_bytes)

    async def __call__(self, scope, receive, send):
        websocket = await websockets.connect(receive=receive, send=send)
        await self.detect_objects(websocket)

    def get(self, request, *args, **kwargs):
        return HttpResponse("This endpoint is for WebSocket connection only.", status=400)





