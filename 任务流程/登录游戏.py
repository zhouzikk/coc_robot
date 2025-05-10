from 主入口 import 任务上下文
from 任务流程.基础任务 import 基础任务


class 移动到目标(基础任务):
    """示例：移动任务"""

    def 执行(self, 上下文: 任务上下文) -> bool:
        print("开始登录中")