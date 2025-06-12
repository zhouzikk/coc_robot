import time
from 任务流程.基础任务框架 import 任务上下文, 基础任务
from 模块.检测.模板匹配器 import 模板匹配引擎


class 等待进入战斗(基础任务):
    """注释字符"""
    def __init__(self):
        super().__init__()
        self.模板识别 = 模板匹配引擎()

    def 执行(self, 上下文: 任务上下文) -> bool:
        """执行进入夜世界的主逻辑"""
        try:
            超时时间 = 30  # 秒
            开始时间 = time.time()

            while time.time() - 开始时间 < 超时时间:

                if self.是否出现换兵种箭头(上下文):
                    上下文.置脚本状态("已进入战斗")
                    return True
                上下文.脚本延时(50)

            raise RuntimeError(f"操作超时：一直卡白云或者某处,导致一直没能进入战斗！已经等待了{超时时间}")
        except RuntimeError as e:
            self.异常处理(上下文, e)
            return False

    def 是否出现换兵种箭头(self,上下文: 任务上下文):
        """验证是否已开始战斗"""
        屏幕图像 = 上下文.op.获取屏幕图像cv(0, 0, 800, 600)
        是否匹配, (x, y), _ = self.模板识别.执行匹配(屏幕图像, "更换兵种箭头[1].bmp|更换兵种箭头[2].bmp", 相似度阈值=0.93)
        if 是否匹配:
            上下文.点击(x-18, y-28)#选中对应兵种
            return True
        else:
            return False

    def 异常处理(self, 上下文: 任务上下文, 异常: Exception):
        super().异常处理(上下文, 异常)
        上下文.发送重启请求(f"任务[{self.__class__.__name__}] 触发了异常：{异常}")


