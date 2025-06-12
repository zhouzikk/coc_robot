import time
from 任务流程.基础任务框架 import 任务上下文, 基础任务
from 任务流程.夜世界打鱼.打开进攻页面任务 import 打开进攻页面
from 任务流程.夜世界打鱼.等待进入战斗 import 等待进入战斗
from 模块.检测.模板匹配器 import 模板匹配引擎


class 夜世界打鱼任务(基础任务):
    """注释字符"""
    def __init__(self):
        super().__init__()
        self.模板识别 = 模板匹配引擎()

    def 执行(self, 上下文: 任务上下文) -> bool:
        """执行进入夜世界的主逻辑"""
        上下文.置脚本状态("夜世界打鱼任务")
        try:
            任务列表 = [
                打开进攻页面(),
                等待进入战斗(),
                # 更多任务...
            ]

            for 索引, 子任务 in enumerate(任务列表, start=1):
                任务名 = type(子任务).__name__
                上下文.置脚本状态(f"[{索引}] {任务名}")
                if not 子任务.执行(上下文):
                    上下文.置脚本状态(f"[失败] 子任务 [{任务名}] 执行失败，终止夜世界打鱼任务链")
                    return False
            return True

        except RuntimeError as e:
            self.异常处理(上下文, e)
            return False

    def 异常处理(self, 上下文: 任务上下文, 异常: Exception):
        super().异常处理(上下文, 异常)
        上下文.发送重启请求(f"任务[{self.__class__.__name__}] 触发了异常：{异常}")


