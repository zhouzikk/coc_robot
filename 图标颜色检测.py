import cv2
import numpy as np


def detect_gray_icons(image_path, icon_positions=None, saturation_thresh=30, value_thresh=50, display=False):
    """
    检测图标是否变为灰色（带调试轮廓绘制）

    参数:
        image_path: 图像路径
        icon_positions: 图标位置列表[(x,y,w,h), ...]，如果为None则自动检测
        saturation_thresh: 饱和度阈值(低于此值认为是灰色)
        value_thresh: 亮度阈值(低于此值认为是黑色而非灰色)
        display: 是否显示处理过程

    返回:
        list: 每个图标是否为灰色的布尔列表
        image: 标记后的图像
    """
    # 1. 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("无法读取图像")

    result_image = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 2. 如果没有提供图标位置，尝试自动检测
    if icon_positions is None:
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 二值化
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        cv2.imshow("asf",binary)
        # 形态学操作
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        # 查找轮廓
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 创建轮廓调试图像
        contour_debug = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contour_debug, contours, -1, (0, 255, 0), 2)

        icon_positions = []
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)

            # 在轮廓调试图像上绘制边界框和编号
            cv2.rectangle(contour_debug, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.putText(contour_debug, str(i), (x, y - 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

            # 筛选可能的图标区域(根据实际情况调整)
            if 20 < w < 100 and 20 < h < 100:
                icon_positions.append((x, y, w, h))
                # 在调试图像上用不同颜色标记被选中的轮廓
                cv2.drawContours(contour_debug, [contour], -1, (255, 0, 0), 2)

        if display:
            # 显示处理过程的中间结果
            cv2.imshow("1. Original Image", image)
            cv2.imshow("2. Binary Image", binary)
            cv2.imshow("3. Contours Detection", contour_debug)

            # 创建选中区域预览
            selected_regions = image.copy()
            for x, y, w, h in icon_positions:
                cv2.rectangle(selected_regions, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("4. Selected Icon Regions", selected_regions)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

    gray_status = []

    # 3. 分析每个图标区域
    for i, (x, y, w, h) in enumerate(icon_positions):
        # 获取图标区域的HSV图像
        icon_region = hsv[y:y + h, x:x + w]

        # 计算平均饱和度和亮度
        avg_saturation = np.mean(icon_region[:, :, 1])
        avg_value = np.mean(icon_region[:, :, 2])

        # 判断是否为灰色
        is_gray = avg_saturation < saturation_thresh and avg_value > value_thresh

        gray_status.append(is_gray)

        # 在图像上标记结果
        color = (0, 0, 255) if is_gray else (0, 255, 0)
        cv2.rectangle(result_image, (x, y), (x + w, y + h), color, 2)
        status_text = f"{i}: Gray(S={avg_saturation:.1f})" if is_gray else f"{i}: Color(S={avg_saturation:.1f})"
        cv2.putText(result_image, status_text,
                    (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    if display:
        cv2.imshow("Final Result", result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return gray_status, result_image


# 使用示例
image_path = "toolbar.png"
gray_status, result_img = detect_gray_icons(image_path, display=True)

print("图标灰度状态:", gray_status)