import cv2
import numpy as np


def detect_gray_rectangles(image_path):
    """
    检测图像中的灰色矩形区域并返回它们的坐标

    参数:
        image_path: 输入图像路径

    返回:
        rectangles: 检测到的矩形坐标列表，每个矩形表示为[x, y, w, h]
        result_image: 标记了矩形区域的图像
    """
    # 1. 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("无法读取图像")
        return [], None

    # 2. 转换为HSV色彩空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #cv2.imshow("a",hsv)
    cv2.waitKey(0)
    # 3. 定义灰色的HSV范围
    # 灰色特征: 低饱和度(0-50), 中等亮度(50-200)
    lower_gray = np.array([0, 0, 50], dtype=np.uint8)
    upper_gray = np.array([180, 50, 200], dtype=np.uint8)

    # 4. 创建灰色掩模
    gray_mask = cv2.inRange(hsv, lower_gray, upper_gray)

    # 5. 形态学操作(可选，用于连接断裂的灰色区域)
    kernel = np.ones((3, 3), np.uint8)
    gray_mask = cv2.morphologyEx(gray_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # 6. 查找轮廓
    contours, _ = cv2.findContours(gray_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 7. 筛选矩形轮廓
    rectangles = []
    result_image = image.copy()

    for cnt in contours:
        # 计算轮廓面积，过滤小噪点
        if cv2.contourArea(cnt) < 5000:  # 可根据需要调整此阈值
            continue

        # 获取边界矩形
        x, y, w, h = cv2.boundingRect(cnt)
        rectangles.append([x, y, w, h])

        # 绘制矩形（使用边界矩形而不是旋转矩形，更稳定）
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 标注矩形坐标
        cv2.putText(result_image, f"({x},{y},{w},{h})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    return rectangles, result_image


# 使用示例
if __name__ == "__main__":
    image_path = "img_1.png"  # 替换为你的图像路径
    rectangles, result_image = detect_gray_rectangles(image_path)

    # 打印检测到的矩形坐标
    print("检测到的灰色矩形区域坐标[x, y, w, h]:")
    for i, rect in enumerate(rectangles, 1):
        print(f"矩形{i}: {rect}")

    # 显示结果
    if result_image is not None:
        cv2.imshow("Detected Gray Rectangles", result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()