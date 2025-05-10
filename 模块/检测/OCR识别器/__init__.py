import threading
from functools import wraps

from .rapidocr_onnxruntime.main import RapidOCR


def 线程安全单例(原始类):
    """
    单例模式装饰器（线程安全版）
    功能：
    1. 保证被装饰的类全局只有一个实例
    2. 所有方法调用自动加锁保证线程安全
    """
    实例容器 = {}
    实例锁 = threading.Lock()  # 控制实例创建的锁

    @wraps(原始类)
    def 包装类(*参数, **配置参数):
        # 双重检查锁定模式（提升性能）
        if 原始类 not in 实例容器:
            with 实例锁:
                if 原始类 not in 实例容器:
                    print(f"创建 {原始类.__name__} 唯一实例")
                    实例容器[原始类] = 原始类(*参数, **配置参数)
        return 实例容器[原始类]

    return 包装类


@线程安全单例
class 安全OCR引擎:
    """RapidOCR的线程安全代理类"""

    def __init__(self, 配置文件路径=None, **配置参数):
        self._操作锁 = threading.Lock()  # 实例方法调用锁
        self._原始引擎 = RapidOCR(配置文件路径, **配置参数)  # 真正的OCR引擎

    def __call__(self, *输入参数, **动态参数):
        """代理所有方法调用并自动加锁"""
        with self._操作锁:
            print("线程安全调用中...")
            return self._原始引擎(*输入参数, **动态参数)

    def __getattr__(self, 属性名):
        """转发其他属性访问到原始引擎"""
        return getattr(self._原始引擎, 属性名)


# 使用示例
if __name__ == "__main__":
    # 第一次创建实例
    引擎1 = 安全OCR引擎(配置文件路径="配置.yaml")

    # 第二次获取的是同一个实例
    引擎2 = 安全OCR引擎()
    print(f"是否是同一个实例: {引擎1 is 引擎2}")  # 输出 True

    # 线程安全调用
    识别结果 = 引擎1("图片.jpg")
    print(识别结果)