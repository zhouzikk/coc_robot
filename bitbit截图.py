import cv2
import numpy as np
from ctypes import windll, byref, create_string_buffer
from ctypes.wintypes import HWND, RECT

def gdi_截图(hwnd):
    # 设置 DPI 感知，确保高分屏正确截图
    windll.user32.SetProcessDPIAware()

    # 获取窗口客户区尺寸
    rect = RECT()
    windll.user32.GetClientRect(hwnd, byref(rect))
    宽, 高 = rect.right, rect.bottom

    # 获取窗口 DC
    屏幕DC = windll.user32.GetDC(hwnd)
    兼容DC = windll.gdi32.CreateCompatibleDC(屏幕DC)
    位图 = windll.gdi32.CreateCompatibleBitmap(屏幕DC, 宽, 高)
    windll.gdi32.SelectObject(兼容DC, 位图)

    # 进行 BitBlt 截图
    SRCCOPY = 0x00CC0020
    windll.gdi32.BitBlt(兼容DC, 0, 0, 宽, 高, 屏幕DC, 0, 0, SRCCOPY)

    # 获取图像字节
    图像总字节数 = 宽 * 高 * 4
    位图信息 = create_string_buffer(图像总字节数)
    windll.gdi32.GetBitmapBits(位图, 图像总字节数, 位图信息)

    # 清理资源
    windll.gdi32.DeleteObject(位图)
    windll.gdi32.DeleteDC(兼容DC)
    windll.user32.ReleaseDC(hwnd, 屏幕DC)

    # 转换为 OpenCV 图像（BGRA 格式）
    图像 = np.frombuffer(位图信息, dtype=np.uint8).reshape((高, 宽, 4))
    return 图像

# 示例：获取窗口句柄（用窗口标题找模拟器）
import win32gui

窗口标题 = "雷电模拟器"  # 替换为你的模拟器窗口标题
窗口句柄 = 526986

if 窗口句柄:
    图像 = gdi_截图(窗口句柄)
    cv2.imshow("GDI截图", 图像)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("找不到窗口，请确认标题正确")
