from new import YOLO检测器

from PIL import Image, ImageDraw, ImageFont

#使用前按安装pip install onnxruntime numpy pillow
def 目标检测(模型路径='ReqFile/yolov5n-7-k5.onnx',
             图片路径=r'ReqFile/bus.jpg',
             是否展示=True,
             字体路径="msyh.ttc",  # 微软雅黑字体路径
             字体大小=10):
    '''
    增强版目标检测，支持在框旁显示类别名称
    '''
    # 初始化检测器（使用示例类别）
    检测器 = YOLO检测器(模型路径, ["金矿", "金库", "圣水采集器", "圣水瓶"])
    检测结果 = 检测器.检测(图片路径)

    if 是否展示:
        # 加载字体（支持中文）
        try:
            字体 = ImageFont.truetype(字体路径, 字体大小)
        except:
            print(f"警告：无法加载字体{字体路径}，使用默认字体")
            字体 = ImageFont.load_default()

        # 打开图片并准备绘图
        原始图片 = Image.open(图片路径)
        绘图工具 = ImageDraw.Draw(原始图片)

        for 目标 in 检测结果:
            # 解包坐标参数
            x1, y1, x2, y2 = 目标['裁剪坐标']
            类别名称 = 目标['类别名称']
            置信度 = 目标.get('置信度', 1.0)  # 兼容无置信度的情况

            # 绘制边界框（红色）
            边框颜色 = (255, 0, 0)
            绘图工具.rectangle([x1, y1, x2, y2], outline=边框颜色, width=3)

            # 准备标签文本
            文本内容 = f"{类别名称} {置信度:.2f}" if '置信度' in 目标 else 类别名称

            # 计算文本位置（框上方）
            文本位置 = (x1, y1 - 字体大小 - 5)  # 上移避免遮挡

            # 绘制文本背景（白色底+黑色边框）
            文本尺寸 = 绘图工具.textbbox((0, 0), 文本内容, font=字体)
            背景框 = [
                文本位置[0] - 2,
                文本位置[1] - 2,
                文本位置[0] + (文本尺寸[2] - 文本尺寸[0]) + 2,
                文本位置[1] + (文本尺寸[3] - 文本尺寸[1]) + 2
            ]
            绘图工具.rectangle(背景框, fill=(255, 255, 255), outline=(0, 0, 0))

            # 绘制文本（黑色）
            绘图工具.text(文本位置, 文本内容, fill=(0, 0, 0), font=字体)

        原始图片.show()

    return 检测结果


if __name__ == "__main__":
    # 使用示例（需要真实字体路径）
    目标检测(
        模型路径="best.onnx",
        图片路径=r"D:\yolo\coc\images\50965031.bmp",
        字体路径="C:/Windows/Fonts/msyh.ttc"  # Windows系统字体路径
    )