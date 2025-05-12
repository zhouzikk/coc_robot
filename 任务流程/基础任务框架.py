

import queue
import random
import threading
import time
from dataclasses import dataclass

from 数据库.任务数据库 import 任务数据库
from 核心.op import op类

from 核心.键盘操作 import 键盘控制器
from 核心.鼠标操作 import 鼠标控制器
from 模块.雷电模拟器操作类 import 雷电模拟器操作类

@dataclass
class 任务上下文:
    机器人标志: str
    数据库: 任务数据库
    消息队列: queue.Queue
    暂停事件: threading.Event
    停止事件: threading.Event
    op:op类
    雷电模拟器:雷电模拟器操作类
    键盘:键盘控制器
    鼠标:鼠标控制器

    def 置脚本状态(self, 日志内容:str, 超时的时间:float=10):
        print(f"[机器人消息] {self.机器人标志} {time.ctime()}: {日志内容}")
        self.数据库.记录日志(self.机器人标志, 日志内容, time.time() + 超时的时间)

    def 发送重启请求(self, 原因: str):
        """发送重启请求并终止当前线程"""
        self.置脚本状态(f"主动请求重启，原因：{原因}")
        # 发送结构化消息到监控中心
        self.消息队列.put({
            "类型": "重启请求",
            "机器人标志": self.机器人标志,
            "原因": 原因
        })

        # 设置停止事件以终止当前线程,正在执行的任务执行到延时时,会判断这个标志,然后触发退出
        self.停止事件.set()

    def 脚本延时(self, 毫秒数):
        for _ in range(毫秒数):
            time.sleep(0.001)


            if self.暂停事件.is_set():
                self.暂停事件.wait()

            if self.停止事件.is_set():
                self.置脚本状态("收到停止事件")
                self.op.安全清理()
                raise SystemExit(f"收到退出请求,主动退出线程,机器人{self.机器人标志}已关闭")

    def 点击(self,x,y,延时=None,是否精确点击=False):
        # 延时默认值
        if 延时 is None:
            延时 = random.randint(400, 600)

        # 精确点击控制
        随机半径 = 0 if 是否精确点击 else 6

        # 加随机偏移
        x = random.randint(x - 随机半径, x + 随机半径)
        y = random.randint(y - 随机半径, y + 随机半径)

        if self.鼠标 is None:
            raise RuntimeError("鼠标控制器未初始化")

        self.鼠标.移动到(x, y)
        self.鼠标.左键点击()
        self.脚本延时(延时)




from abc import ABC, abstractmethod


class 基础任务(ABC):
    """游戏任务基类"""

    @abstractmethod
    def 执行(self, 上下文: '任务上下文') -> bool:
        """
        返回True继续下一个任务，返回False终止流程
        """
        pass

    def 异常处理(self, 上下文: '任务上下文', 异常: Exception):
        上下文.置脚本状态(f"任务[{self.__class__.__name__}] 异常：{异常}")
