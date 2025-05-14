import functools
import time


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