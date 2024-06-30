import subprocess


def detect_objects(self, frame_data):
    # 调用 YOLOv5 命令行接口进行目标检测
    result = subprocess.run(['python', 'D:\yolov5-master\detect.py', '--stream', frame_data], capture_output=True)
    # 检测结果保存在 result.stdout 中，可以对其进行处理
    return result.stdout