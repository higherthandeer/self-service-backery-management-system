import pickle
import socket
import threading
import cv2
import base64

video_source = 0
# 创建视频捕获对象
cap = cv2.VideoCapture(video_source)
# 获取视频的宽度和高度
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 用于存储连接的客户端 Socket
client_sockets = []
import random

# 生成一个包含19个随机整数的列表


# 创建 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定服务器地址和端口
server_address = ('192.168.157.195', 5000)
server_socket.bind(server_address)

# 监听客户端连接
server_socket.listen(1)


def image_to_base64(image):
    # 将图像数据编码为 Base64 字符串
    image_base64 = base64.b64encode(image).decode('utf-8')
    return image_base64


# 定义发送视频数据的函数
def send_video_data():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 将图像编码为 JPEG 格式
        _, image_data = cv2.imencode('.jpg', frame)
        # 遍历所有客户端连接，发送视频数据
        for client_socket in client_sockets:
            try:
                # 发送图像数据
                encoded_data = pickle.dumps({
                    "leftimg": image_to_base64(image_data),
                })

                client_socket.sendall(encoded_data)
            except Exception as e:
                print(f"Error sending video data to client: {e}")
                client_socket.close()
                client_sockets.remove(client_socket)


# 定义处理客户端连接的函数
def handle_client_connection(client_socket):
    while True:
        try:
            # 接收客户端请求
            data = client_socket.recv(1024)
            if not data:
                break
            # 处理客户端请求
            # 在此可以添加其他自定义逻辑
        except Exception as e:
            print(f"Error handling client connection: {e}")
            break

    # 关闭客户端连接
    client_socket.close()
    client_sockets.remove(client_socket)


# 接受客户端连接，并启动视频发送线程
def accept_client_connections():
    while True:
        client_socket, _ = server_socket.accept()
        client_sockets.append(client_socket)


# 启动视频发送线程和客户端连接接受线程
send_thread = threading.Thread(target=send_video_data)
accept_thread = threading.Thread(target=accept_client_connections)

send_thread.start()
accept_thread.start()
