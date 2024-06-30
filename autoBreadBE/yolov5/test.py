from pathlib import Path
import os
from YOLOV5 import run
# 获取当前文件的路径

current_file = Path(__file__).resolve()

# 获取当前项目的根目录
root_directory = current_file.parents[1]
print(root_directory)

#
# wp = [root_directory, '/yolov5/best.pt']  # 权重路径
imgp = root_directory / 'media' / 'donuts_236_jpg.rf.0020fbff53095876e2b8f89cf1c8da42.jpg'
print(imgp)
run(weights='best.pt', source=imgp)