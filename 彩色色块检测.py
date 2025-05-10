import cv2
import numpy as np


def optimize_icon_detection(image_path, display=False):
    """
    优化后的矩形图标检测方法

    参数:
        image_path: 图像路径
        display: 是否显示检测过程

    返回:
        list: 检测到的图标位置[(x,y,w,h), ...]
        image: 标记后的结果图像
    """
    # 1. 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("无法读取图像")

    original = image.copy()
    height, width = image.shape[:2]

    # 2. 预处理 - 使用HSV的饱和度通道增强图标边缘
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    blurred = cv2.GaussianBlur(saturation, (5, 5), 0)

    # 3. 自适应Canny边缘检测
    median = np.median(blurred)
    lower = int(max(0, 0.7 * median))
    upper = int(min(255, 1.3 * median))
    edges = cv2.Canny(blurred, lower, upper)

    # 4. 边缘后处理
    kernel = np.ones((3, 3), np.uint8)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # 5. 查找并筛选轮廓
    contours, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 6. 多级筛选矩形图标
    icon_candidates = []
    for contour in contours:
        # 基本筛选：面积和周长
        area = cv2.contourArea(contour)
        if area < 3000 or area > 10000:  # 根据实际调整
            continue

        # 多边形逼近
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * peri, True)

        # 必须是四边形
        if len(approx) != 4:
            continue

        # 获取最小外接矩形
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int8(box)

        # 计算矩形特征
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        rectangularity = area / (w * h)

        # 综合筛选条件
        if (30 < w < 150 and 30 < h < 150 and  # 尺寸范围
                0.85 < rectangularity < 1.1 and  # 矩形完整度
                0.8 < aspect_ratio < 1.2 and  # 宽高比
                cv2.isContourConvex(approx)):  # 凸形检测
            icon_candidates.append((x, y, w, h, box))

    # 7. 基于空间分布进一步筛选（工具栏图标通常水平/垂直排列）
    filtered_icons = []
    if icon_candidates:
        # 按x坐标排序（假设水平排列）
        icon_candidates.sort(key=lambda x: x[0])

        # 计算平均高度和间距
        avg_height = np.mean([h for _, _, h, _, _ in icon_candidates])

        # 筛选位置和大小相近的图标
        prev_x = -100
        for x, y, w, h, box in icon_candidates:
            # 与平均高度比较
            if 0.7 * avg_height < h < 1.3 * avg_height:
                # 检查与上一个图标的间距
                if x - prev_x > 0 and (x - prev_x < 2 * avg_height or prev_x == -100):
                    filtered_icons.append((x, y, w, h))
                    prev_x = x + w

    # 8. 可视化结果
    result_image = original.copy()
    debug_images = []

    # 绘制所有候选矩形（黄色）
    for x, y, w, h, box in icon_candidates:
        cv2.drawContours(result_image, [box], 0, (0, 255, 255), 2)

    # 绘制最终筛选结果（绿色）
    for i, (x, y, w, h) in enumerate(filtered_icons):
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(result_image, f"Icon {i}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    if display:
        # 创建调试图像
        debug_images.append(("1. Original", original))
        debug_images.append(("2. Saturation Channel", saturation))
        debug_images.append(("3. Blurred", blurred))
        debug_images.append(("4. Canny Edges", edges))
        debug_images.append(("5. Closed Edges", closed_edges))

        # 轮廓调试图
        contour_debug = np.zeros_like(original)
        cv2.drawContours(contour_debug, contours, -1, (0, 255, 0), 1)
        debug_images.append(("6. All Contours", contour_debug))

        debug_images.append(("7. Final Detection", result_image))

        # 显示调试图像
        for name, img in debug_images:
            cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return filtered_icons, result_image


# 使用示例
image_path = "toolbar.png"
detected_icons, result_img = optimize_icon_detection(image_path, display=True)

print(f"检测到 {len(detected_icons)} 个图标:")
for i, (x, y, w, h) in enumerate(detected_icons):
    print(f"图标 {i}: 位置({x},{y}), 尺寸({w}x{h})")