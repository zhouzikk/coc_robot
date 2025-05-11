import io
import ctypes
import os
import time
import win32com.client
from PIL import Image
import numpy as np
import cv2

from 核心.核心异常们 import 图像获取失败

当前文件所在目录 = os.path.dirname(__file__)  # 当前文件所在目录
print(当前文件所在目录)

# 加载注册com组件的dll
免注册dll = ctypes.windll.LoadLibrary(当前文件所在目录+R"\op-0.4.5_with_model\tools.dll")
dll目录=当前文件所在目录+R"\op-0.4.5_with_model\op_x64.dll"
是否注册成功 = 免注册dll.setupW(dll目录)

print("op免注册状态：" + str(是否注册成功))

import threading

class COM对象管理器:
    """COM对象管理器（线程安全）"""
    线程数据 = threading.local()

    @classmethod
    def 初始化COM(cls):
        if not hasattr(cls.线程数据, "已初始化"):
            import pythoncom
            pythoncom.CoInitialize()
            cls.线程数据.已初始化 = True

    @classmethod
    def 释放COM(cls):
        if hasattr(cls.线程数据, "已初始化"):
            import pythoncom
            pythoncom.CoUninitialize()
            del cls.线程数据.已初始化


class op类:
    def __init__(self, 窗口句柄, 图像获取模式='opengl'):
        COM对象管理器.初始化COM()
        self.op_COM对象 = win32com.client.Dispatch("op.opsoft")

        # op插件bug,第一次截图可能会弹出报错,后面截图就好了,所以将报错信息设置为控制台输出
        self.op_COM对象.SetShowErrorMsg(3)

        self.是否已绑定 = False  # 新增绑定状态标志
        if 窗口句柄:
            self.绑定(窗口句柄, 图像获取模式)


    def 绑定(self, 窗口句柄, 图像获取模式, 鼠标模式="normal", 键盘模式="normal", 模式=0):
        绑定结果 = self.op_COM对象.BindWindow(窗口句柄, 图像获取模式, 鼠标模式, 键盘模式, 模式)

        if 绑定结果 != 1:
            raise RuntimeError(f"窗口绑定失败，错误码：{绑定结果}")
        self.是否已绑定 = True
        print("窗口绑定成功")
        return 绑定结果

    def _解绑(self):
        """安全解除窗口绑定"""
        if self.是否已绑定:
            解绑结果 = self.op_COM对象.UnBindWindow()
            if 解绑结果 != 1:
                raise RuntimeError(f"解绑失败，错误码：{解绑结果}")
            self.是否已绑定 = False
            print("窗口解绑成功")

    def 安全清理(self):
        """安全释放所有资源,并解绑窗口"""
        try:
            self._解绑()
            if hasattr(self, 'op_COM对象') and self.op_COM对象 is not None:

                del self.op_COM对象
                self.op_COM对象 = None
                import gc
                gc.collect()
        finally:
            COM对象管理器.释放COM()

    def __del__(self):
        """析构函数自动解绑"""
        self.安全清理()

    def 获取屏幕图像cv(self, 左边=0, 顶边=0, 右边=2000, 底边=2000):
        """返回OpenCV格式的numpy数组图像（自动重试黑屏检测）"""
        最大重试次数 = 3
        黑屏阈值 = 5  # 可调整的亮度阈值（0-255）
        重试间隔 = 0.05  # 单位：秒

        for 尝试次数 in range(1, 最大重试次数 + 1):
            # 获取屏幕数据
            结果, 数据指针, 数据大小 = self.op_COM对象.GetScreenDataBmp(左边, 顶边, 右边, 底边)
 
            # 基础有效性检查
            if not 结果 or 数据大小 < 1024:  # 假设有效图像数据至少1KB
                if 尝试次数 < 最大重试次数:
                    time.sleep(重试间隔)
                    continue

                raise RuntimeError("连续获取屏幕数据失败")

            # 转换字节数据
            指针对象 = ctypes.c_void_p(数据指针)
            字节数组类型 = (ctypes.c_char * 数据大小)
            字节数据 = ctypes.cast(指针对象, ctypes.POINTER(字节数组类型)).contents

            try:
                with io.BytesIO(字节数据) as 字节流:
                    # 转换图像格式
                    pil_image = Image.open(字节流)
                    cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

                    # 黑屏检测（优化性能版）
                    灰度图 = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                    if cv2.mean(灰度图)[0] > 黑屏阈值:
                        return cv_image

            except Exception as 转换异常:
                if 尝试次数 == 最大重试次数:

                    raise RuntimeError(f"图像转换异常: {str(转换异常)}")

            # 达到最大尝试次数前进行延迟
            if 尝试次数 < 最大重试次数:
                time.sleep(重试间隔)
        # 超出最大重试次数

        raise 图像获取失败(f"连续{最大重试次数}次获取到黑屏图像")

    def __getattr__(self, 属性名):
        """转发其他属性访问到原始引擎"""
        return getattr(self.op_COM对象, 属性名)

if __name__ == "__main__":

    op=op类(265386)
    # 获取OpenCV格式图像
    cv图像 = op.获取屏幕图像cv(0, 0, 800, 600)
    cv2.imshow('屏幕截图', cv图像)
    cv2.waitKey(0)


    cv图像 = op.获取屏幕图像cv(0, 0, 800, 600)
    cv2.imshow('屏幕截图', cv图像)
    cv2.waitKey(0)

    cv图像 = op.获取屏幕图像cv(0, 0, 800, 600)
    cv2.imshow('屏幕截图', cv图像)
    cv2.waitKey(0)

    cv图像 = op.获取屏幕图像cv(0, 0, 800, 600)
    cv2.imshow('屏幕截图', cv图像)
    cv2.waitKey(0)

    cv图像 = op.获取屏幕图像cv(0, 0, 800, 600)
    cv2.imshow('屏幕截图', cv图像)
    cv2.waitKey(0)

    # 获取原始字节数据
    图像字节数据 = op.获取屏幕图像字节数据(0, 0, 800, 600)
    with open('screen.bmp', 'wb') as f:
        f.write(图像字节数据)