import asyncio
import json

import cv2
import base64

from asgiref.sync import sync_to_async

from .models import Goods

from channels.generic.websocket import AsyncWebsocketConsumer
from yolov5.YOLOV5 import run
from autoBreadBE.utils.decimalJSON import DecimalEncoder


class YOLOv5Consumer(AsyncWebsocketConsumer):
    cap = None

    async def connect(self):
        await self.accept()

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()  # ret(布尔值)，:表示是否成功读取到图像帧 frame: 则是读取到的图像帧数据。
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)  # 将图像帧编码为JPEG格式
                # print(type(buffer))
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                # print(type(frame_base64))
                detection_result = self.detect_objects(frame_base64)
                # print(detection_result)
                await self.send(detection_result)
            await asyncio.sleep(0.05)  # 每秒钟发送一次

    async def disconnect(self, close_code):
        if self.cap:
            self.cap.release()

    async def receive(self, text_data):
        if text_data == 'close':
            self.cap.release()
            await self.close()

    def detect_objects(self, frame_base64):
        # 将图像数据写入临时文件
        temp_file_path = r'D:\autoBread\autoBreadBE\media\temp.jpg'
        with open(temp_file_path, 'wb') as f:
            f.write(base64.b64decode(frame_base64))

        # 调用命令行执行 YOLOv5 检测

        detection_result = run(source=temp_file_path)
        return detection_result


class SaleConsumer(AsyncWebsocketConsumer):
    cap = None

    async def connect(self):
        await self.accept()

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()  # ret(布尔值)，:表示是否成功读取到图像帧 frame: 则是读取到的图像帧数据。
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)  # 将图像帧编码为JPEG格式
                # print(type(buffer))
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                # print(type(frame_base64))
                detection_result = self.detect_objects(frame_base64)
                detection_result_dict = json.loads(detection_result)
                detect_objects = detection_result_dict['txt']
                # 新建一个空列表用于存储带价格的检测结果
                temp = []
                for obj in detect_objects:
                    name = obj['name']
                    price = await self.get_goods_price(name)
                    obj['price'] = price
                    temp.append(obj)
                detection_result_dict['txt'] = temp
                detection_result = detection_result_dict

                result = json.dumps(detection_result, cls=DecimalEncoder)
                await self.send(result)
            await asyncio.sleep(1)  # 每秒钟发送一次

    async def disconnect(self, close_code):
        if self.cap:
            self.cap.release()

    async def receive(self, text_data):
        if text_data == 'close':
            self.cap.release()
            await self.close()

    def detect_objects(self, frame_base64):
        # 将图像数据写入临时文件
        temp_file_path = r'D:\autoBread\autoBreadBE\media\temp.jpg'
        with open(temp_file_path, 'wb') as f:
            f.write(base64.b64decode(frame_base64))

        # 调用命令行执行 YOLOv5 检测

        detection_result = run(source=temp_file_path)
        return detection_result

    @sync_to_async
    def get_goods_price(self, name):
        goods_list = Goods.objects.filter(breadname=name, is_expired=False)
        if goods_list.exists():
            first_good = goods_list.first()
            return first_good.price
        else:
            # 如果没有找到满足条件的面包，可以返回一个默认值或者抛出异常
            return None  # 或者抛出异常，比如 ValueError("No goods found with the given name and not expired.")

