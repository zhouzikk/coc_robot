import cv2
import numpy as np


def detect_white_box(image_path, min_area=1000, threshold=200):
    """
    检测图像中是否存在白色框

    参数:
        image_path: 图像路径
        min_area: 最小区域面积(过滤小噪声)
        threshold: 白色阈值(0-255)

    返回:
        bool: 是否检测到白色框
        image: 标记后的图像(用于可视化)
    """
    # 1. 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("无法读取图像")

    # 2. 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. 二值化处理 - 提取白色区域
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    cv2.imshow("12",binary)
    cv2.waitKey(0)
    # 4. 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    has_white_box = False

    # 5. 遍历轮廓并筛选
    for contour in contours:
        # 计算轮廓面积
        area = cv2.contourArea(contour)

        # 忽略太小的区域
        if area < min_area:
            continue

        # 多边形逼近
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # 检查是否是四边形(4个顶点)
        if len(approx) == 4:
            # 计算轮廓的宽高比
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            # 宽高比在一定范围内才认为是矩形(可根据需要调整)
            if 0.7 < aspect_ratio < 1.3:
                has_white_box = True
                # 在原图上绘制矩形(可选)
                cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)

    return has_white_box, image


# 使用示例
image_path = "img_1.png"
has_box, result_image = detect_white_box(image_path)

if has_box:
    print("检测到白色框")
    cv2.imshow("Result", result_image)
    cv2.waitKey(0)
else:
    print("未检测到白色框")