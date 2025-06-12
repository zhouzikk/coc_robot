import functools
import time

import cv2


def 打印运行耗时(函数):
    @functools.wraps(函数)
    def 包装器(*参数, **关键字参数):
        开始时间 = time.time()
        结果 = 函数(*参数, **关键字参数)
        结束时间 = time.time()
        耗时 = 结束时间 - 开始时间
        print(f"函数「{函数.__name__}」运行耗时：{耗时:.4f} 秒")
        return 结果
    return 包装器


def 生成贝塞尔轨迹(起点, 控制点1, 控制点2, 终点, 步数=30):
    """生成三阶贝塞尔曲线路径"""
    轨迹 = []
    for i in range(步数 + 1):
        t = i / 步数
        x = (1 - t) ** 3 * 起点[0] + 3 * (1 - t) ** 2 * t * 控制点1[0] + 3 * (1 - t) * t ** 2 * 控制点2[
            0] + t ** 3 * 终点[0]
        y = (1 - t) ** 3 * 起点[1] + 3 * (1 - t) ** 2 * t * 控制点1[1] + 3 * (1 - t) * t ** 2 * 控制点2[
            1] + t ** 3 * 终点[1]
        轨迹.append((int(x), int(y)))
    return 轨迹

def 显示图像(屏幕图像):
    cv2.imshow("test",屏幕图像)
    cv2.waitKey(0)
    cv2.destroyAllWindows()