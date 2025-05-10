from abc import ABC, abstractmethod

from 主入口 import 任务上下文


class 基础任务(ABC):
    """游戏任务基类
    所有业务步骤需继承此接口"""

    @abstractmethod
    def 执行(self, 上下文: '任务上下文') -> bool:
        """
        返回True继续下一个任务，返回False终止流程
        """
        pass

    def 异常处理(self, 上下文: '任务上下文', 异常: Exception):
        """默认异常处理"""
        上下文.全局消息队列.put(f"任务[{self.__class__.__name__}] 异常: {str(异常)}")