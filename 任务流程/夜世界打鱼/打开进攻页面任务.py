from 任务流程.基础任务框架 import 任务上下文
from 任务流程.夜世界打鱼.夜世界基础任务 import 夜世界基础任务
from 模块.检测.模板匹配器 import 模板匹配引擎


class 打开进攻页面(夜世界基础任务):
    def __init__(self ,上下文: '任务上下文'):
        super().__init__(上下文)


    def 执行(self) -> bool:

        try:
            self.上下文.点击(58, 536, 700)  # 点击进攻
            if not self.是否出现开始进攻():
                raise RuntimeError("打开进攻页面失败")

            self.上下文.点击(600, 380)  # 点击立即寻找

            return True

        except RuntimeError as e:
            self.异常处理(e)
            return False
    def 是否出现开始进攻(self):
        """验证是否已开始战斗"""
        是否匹配, (x, y)= self.是否出现图片( "夜世界_开始进攻.bmp")
        if 是否匹配:
            return True
        else:
            return False

    def 异常处理(self, 异常: Exception,**关键字参数):
        super().异常处理(异常)
        self.上下文.发送重启请求(f"任务[{self.__class__.__name__}] 触发了异常：{异常}")

