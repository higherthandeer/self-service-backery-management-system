import argparse  # 解析命令行参数的库
import base64
import json
import os  # 与操作系统进行交互的文件库，包含文件路径操作与解析
import platform  # 用于获取操作系统相关信息，根据不同的操作系统执行不同的操作
import sys  # sys模块包含了与python解释器和他的环境有关的函数
from pathlib import Path  # Path能够更加方便地对字符串路径进行处理
import io
import torch
import numpy as np

FILE = Path(__file__).resolve()  # 获取当前文件的绝对路径 D://yolov5-master/train.py
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:  # sys.path即当前python环境可以运行的路径,假如当前项目不在该路径中,就无法运行其中的模块,所以就需要加载路径
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode


@smart_inference_mode()
def run(
        weights=ROOT / 'best.pt',  # 权重文件
        source=ROOT / 'data/images',  # 测试图片所在的文件夹或文件路径
        data=ROOT / 'bread/bread_parameter.yaml',  # 含有数据集相关信息的dataset.yaml所在的路径
        imgsz=(640, 640),  # 预测推理时图片的大小(height, width)
        conf_thres=0.25,  # 置信度值
        iou_thres=0.45,  # NMS IOU 阈值
        max_det=1000,  # 每张图最大检测数量，默认是最多检测1000个目标
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=True,  # # 检测的时候是否实时的把检测结果显示出来，默认False。
        save_txt=False,  # 是否把检测结果保存成一个.txt的YOLO格式，默认False。
        save_conf=False,  # 上面保存的txt中是否包含置信度，默认False。
        save_crop=False,  # 是否把模型检测的物体裁剪下来，默认False。
        nosave=False,  # 不保存预测的结果，默认False。
        classes=None,  # 指定检测某几种类别。比如coco128.yaml中person是第一个类别，classes指定“0”，则表示只检测图片中的person。
        agnostic_nms=False,
        # 跨类别nms。比如待检测图像中有一个长得很像排球的足球，pt文件的分类中有足球和排球两种，那在识别时这个足球可能会被同时框上2个框：一个是足球，一个是排球。开启agnostic-nms后，那只会框出一个框，默认False。
        augment=False,  # 数据增强，默认False。
        visualize=False,  # 是否可视化特征图。如果开启了这和参数可以看到exp文件夹下又多了一些文件，这里.npy格式的文件就是保存的模型文件，可以使用numpy读写。还有一些png文件，默认False。
        update=False,  # update：如果指定这个参数，则对所有模型进行strip_optimizer操作，去除pt文件中的优化器等信息，默认False。
        project=ROOT / 'runs/detect',  # # 预测结果保存的路径
        name='exp',  # # 预测结果保存文件夹名
        exist_ok=False,  # 每次预测模型的结果是否保存在原来的文件夹。如果指定了这个参数的话，那么本次预测的结果还是保存在上一次保存的文件夹里；如果不指定就是每次预测结果保存一个新的文件夹下，默认False。
        line_thickness=3,  # 调节预测框线条粗细的，default=3。
        hide_labels=False,  # 隐藏预测图片上的标签（只有预测框），默认False。
        hide_conf=False,  # 隐藏置信度（还有预测框和类别信息，但是没有置信度），默认False。
        half=False,
        # 是否使用 FP16 半精度推理，默认False。在training阶段，梯度的更新往往是很微小的，需要相对较高的精度，一般要用到FP32以上。在inference的时候，精度要求没有那么高，一般F16（半精度）就可以，甚至可以用INT8（8位整型），精度影响不会很大。同时低精度的模型占用空间更小了，有利于部署在嵌入式模型里面。
        dnn=False,  # 是否使用 OpenCV DNN 进行 ONNX 推理，默认False
        vid_stride=1,  # video frame-rate stride
):
    # 读取模型
    device = select_device(device)
    # DetectMultiBackend定义在models.common模块中，是我们要加载的网络，
    # weights: 模型的权重路径（比如yolov5s.pt） device: 设备 dnn: 是否使用OpenCV data:数据模型如data.yaml fp16: 是否使用半精度浮点数进行推理
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    '''
          stride：推理时所用到的步长，默认为32， 大步长适合于大目标，小步长适合于小目标
          names：保存推理结果名的列表，比如默认模型的值是['person', 'bicycle', 'car', ...] 
          pt: 加载的是否是pytorch模型（也就是pt格式的文件）
    '''
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader数据读取器
    bs = 1  # batch_size
    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    # Run inference 预测推理 热身部分
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup，模型预热
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())  # dt: 存储每一步骤的耗时 seen: 计数功能，已经处理完了多少帧图片
    for path, im, im0s, vid_cap, s in dataset:  # 遍历数据集
        '''
        在dataset中，每次迭代的返回值是self.sources, img, img0, None, ''
        path：文件路径（即source）
        im: resize后的图片（经过了放缩操作）
        im0s: 原始图片
        vid_cap=none
        s： 图片的基本信息，比如路径，大小
        '''
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()
            im /= 255  # 0 - 255 to 0.0 - 1.0 归一化
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim 扩展维度[channel,width,height]->[None,channel,width,height]缺少batch这个尺寸

        # Inference推理
        with dt[1]:
            # 可视化文件路径。如果为True则保留推理过程中的特征图，保存在runs文件夹中
            # visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            # 推理结果，pred保存的是所有的bound_box的信息，
            pred = model(im, augment=augment, visualize=visualize)  # 直接调用了forward()

        # NMS非极大抑制，返回值为过滤后的预测框，除去多余的框
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        '''
        pred: 网络的输出结果
        conf_thres： 置信度阈值
        iou_thres： iou阈值
        classes: 是否只保留特定的类别 默认为None
        agnostic_nms： 进行nms是否也去除不同类别之间的框
        max_det: 检测框结果的最大数量 默认1000
        '''
        # print('pred',pred)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions 预测过程
        # 把所有的检测框画到原图中
        for i, det in enumerate(pred):  # per image i:每个batch的信息，det: 表示5个检测框的信息
            seen += 1
            p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
            '''
            大部分我们一般都是从LoadImages流读取本都文件中的照片或者视频 所以batch_size=1
            p: 当前图片/视频的绝对路径 如 F:\yolo_v5\yolov5-U\data\images\bus.jpg
            s: 输出信息 初始为 ''
            im0: 原始图片 letterbox + pad 之前的图片
            frame: 视频流,此次取的是第几张图片
            '''
            # print('p, im0, frame',p, im0, frame)

            p = Path(p)
            # print('p',p)
            # save_path = str(save_dir / p.name)  # im.jpg # to Path # 图片/视频的保存路径save_path 如 runs\\detect\\exp8\\fire.jpg
            # # print('save_path',save_path)
            # txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt # 设置保存框坐标的txt文件路径，每张图片对应一个框坐标信息
            # print('txt_path',txt_path)
            s += '%gx%g ' % im.shape[2:]  # print string # 设置输出图片信息。图片shape (w, h)
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh # 得到原图的宽和高

            # 保存截图。如果save_crop的值为true，则将检测到的bounding_box单独保存成一张图片。
            imc = im0.copy() if save_crop else im0  # for save_crop

            # 得到一个绘图的类，类中预先存储了原图、线条宽度、类名
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            # print('annotator',annotator)
            txt_ob = []
            # 判断有没有框
            if len(det):
                # Rescale boxes from img_size to im0 size
                # 将预测信息映射到原图
                # 将标注的bounding_box大小调整为和原图一致（因为训练时原图经过了放缩）此时坐标格式为xyxy
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results打印结果
                # Print results
                # 返回检测到的物体和数量

                # 打印检测到的类别数量
                for c in det[:, 5].unique():
                    n = int((det[:, 5] == c).sum())  # detections per class
                    class_name = names[int(c)]
                    txt_ob.append({
                        "name": turn_chinese(class_name),
                        "count": n
                    })
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results写入结果
                # 保存预测结果：txt/图片画框/crop-image
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        # 将xyxy(左上角+右下角)格式转为xywh(中心点+宽长)格式，并归一化，转化为列表再保存
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        # line的形式是： ”类别 x y w h“，若save_conf为true，则line的形式是：”类别 x y w h 置信度“
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format

                    # 在原图上画框+将预测到的目标剪切出来保存成图片，保存在save_dir/crops下，在原图像画图或者保存结果

                    c = int(cls)  # integer class # 类别标号
                    label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')  # 类别名
                    annotator.box_label(xyxy, label, color=colors(c, True))  # 绘制边框

            # Stream results
            # 如果设置展示，则show图片 / 视频
            im0 = annotator.result()  # im0是绘制好的图片
            # if view_img:
            #     cv2.imshow(str(p), im0)
            #     cv2.waitKey(1)  # 1 millisecond # 暂停 1 millisecond
            _, buffer = cv2.imencode('.jpg', im0)
            img_ob = base64.b64encode(buffer).decode('utf-8')
            # print(result)
            # LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")
            #
            # Print results
            # t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
            # LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
            data = {'img': img_ob, 'txt': txt_ob}
            result = json.dumps(data)
            return result
            # print(type(im0))
            # with io.BytesIO() as output:
            #     np.save(output, im0)  # 保存数组为字节流
            #     array_bytes = output.getvalue()  # 获取字节流的值
            # return im0
            # 显示图片

    #
    #         # Save results (image with detections)
    #         # 设置保存图片/视频
    #
    # Print time (inference-only)


def turn_chinese(name):
    mapping = {
        'Baguette': "法棍",
        'Croissant': '牛角包',
        'Donuts': '甜甜圈',
        'LayerCake': '千层蛋糕',
        'Sandwich': '三明治',
    }
    return mapping.get(name, None)

def main():
    pass


if __name__ == "__main__":
    main()
