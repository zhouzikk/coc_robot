from 任务流程.基础任务框架 import 基础任务, 任务上下文
from 模块.检测.模板匹配器 import 模板匹配引擎


class 打开进攻页面(基础任务):
    def __init__(self):
        super().__init__()
        self.模板识别 = 模板匹配引擎()

    def 执行(self, 上下文: 任务上下文) -> bool:

        try:
            上下文.点击(58, 536, 700)  # 点击进攻
            if not self.是否出现开始进攻(上下文):
                raise RuntimeError("打开进攻页面失败")

            上下文.点击(600, 380)  # 点击立即寻找

            return True

        except RuntimeError as e:
            self.异常处理(上下文, e)
            return False
    def 是否出现开始进攻(self,上下文: 任务上下文):
        """验证是否已开始战斗"""
        屏幕图像 = 上下文.op.获取屏幕图像cv(0, 0, 800, 600)
        是否匹配, (x, y), _ = self.模板识别.执行匹配(屏幕图像, "夜世界_开始进攻.bmp", 相似度阈值=0.9)
        if 是否匹配:
            return True
        else:
            return False
    def 异常处理(self, 上下文: 任务上下文, 异常: Exception):
        super().异常处理(上下文, 异常)
        上下文.发送重启请求(f"任务[{self.__class__.__name__}] 触发了异常：{异常}")

