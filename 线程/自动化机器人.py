import queue
import threading
import time

import cv2

from 核心.核心异常们 import 图像获取失败
from 数据库.任务数据库 import 任务数据库
from 核心.op import op类
from 模块.雷电模拟器操作类 import 雷电模拟器操作类


class 自动化机器人:
    """为单个用户提供游戏自动化服务的机器人实例"""

    def __init__(self, 机器人标志: str, 消息队列: queue.Queue, 数据库: 任务数据库):
        # 基础属性
        self.机器人标志 = 机器人标志
        self.消息队列 = 消息队列#用来给监控中心发送消息
        self.数据库 = 数据库


        self.是否暂停 = False
        self.是否停止 = True
        self.雷电模拟器=雷电模拟器操作类(self.数据库.获取机器人设置(机器人标志).雷电模拟器索引)
        self.op:op类


    def 启动(self):
        self.主线程 = threading.Thread(
            target=self._任务流程,
            name=f"任务线程-{self.机器人标志}",
            daemon=True
        )
        self.主线程.start()
        self.是否停止 = False

    def _任务流程(self):
        """主任务逻辑"""
        try:
            # 执行任务阶段
            self._执行阶段()
        except Exception as e:
            #异常会导致停止执行脚本,不会进一步记录日志
            #然后会被监控中心检测到无心跳，导致重启
            self._往数据库写日志(f"异常: {str(e)}",0)
            #self.消息队列.put(f"用户{self.用户标识} 异常: {str(e)}")

    def _执行阶段(self):
        """任务处理逻辑"""
        self.op = op类(self.雷电模拟器.取绑定窗口句柄的下级窗口句柄())
        self._往数据库写日志("开始执行",20242)
        #获取OpenCV格式图像
        try:
            cv图像 = self.op.获取屏幕图像cv(0, 0, 800, 600)
            cv2.imshow('屏幕截图', cv图像)
            cv2.waitKey(0)

        except 图像获取失败 as 异常实例:
            print("处理异常")
            raise 异常实例

    def _往数据库写日志(self,日志内容:str,超时的时间:float=10):
        print(f"用户{self.机器人标志} {time.ctime()}: {日志内容}")
        self.数据库.记录日志(self.机器人标志, 日志内容, time.time() + 超时的时间)


    def 检查超时(self) -> bool:
        """检查是否超时,返回False未超时,返回True则超时"""

        最后日志 = self.数据库.读取最后日志(self.机器人标志)
        if not 最后日志:
            return False  # 无日志视为需要启动

        if self.是否停止==True:
            return False

        return time.time() > 最后日志.下次超时 if 最后日志 else False

    def 停止(self):
        """停止线程"""
        self.已停止 = True
        if self.主线程.is_alive():
            self.主线程.join()
        self.状态 = "已停止"
