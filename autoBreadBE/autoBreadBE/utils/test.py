from pathlib import Path

# 获取当前文件的路径
current_file = Path(__file__).resolve()

# 获取当前项目的根目录
root_directory = current_file.parents[2]
# print(root_directory)


wp = [root_directory, '/yolov5/best.pt']  # 权重路径
imgp = [root_directory, '/media/donuts_236_jpg.rf.0020fbff53095876e2b8f89cf1c8da42.jpg']  # 图片路径

# run(weights=wp, source=imgp)
