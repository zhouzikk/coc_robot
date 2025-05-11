import queue
import threading
import time
from dataclasses import dataclass

import cv2

from 核心.核心异常们 import 图像获取失败
from 数据库.任务数据库 import 任务数据库, 机器人设置
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

    def 日志记录器(self,日志内容:str,超时的时间:float=10):
        print(f"[机器人消息] {self.机器人标志} {time.ctime()}: {日志内容}")
        self.数据库.记录日志(self.机器人标志, 日志内容, time.time() + 超时的时间)

    def 发送重启请求(self, 原因: str):
        """发送重启请求并终止当前线程"""
        self.日志记录器(f"主动请求重启，原因：{原因}")
        # 发送结构化消息到监控中心
        self.消息队列.put({
            "类型": "重启请求",
            "机器人标志": self.机器人标志,
            "原因": 原因
        })

        # 设置停止事件以终止当前线程
        self.停止事件.set()

    def 延时(self,毫秒数):
        for _ in range(毫秒数):
            time.sleep(0.001)


            if self.暂停事件.is_set():
                self.暂停事件.wait()

            if self.停止事件.is_set():
                self.日志记录器("收到停止事件")
                self.op.安全清理()
                raise SystemExit(f"收到退出请求,主动退出线程,机器人{self.机器人标志}已关闭")




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
        """默认异常处理"""
        上下文.消息队列.put(f"任务[{self.__class__.__name__}] 异常: {str(异常)}")






class 启动游戏(基础任务):

    def 执行(self, 上下文: '任务上下文') -> bool:

        上下文.日志记录器("开始启动游戏")
        cv图像=上下文.op.获取屏幕图像cv(0, 0, 800, 600)

        上下文.延时(300)
        cv2.imshow('屏幕截图', cv图像)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return True


class 自动化机器人:
    """为单个用户提供游戏自动化服务的机器人实例"""

    def __init__(self, 机器人标志: str, 消息队列: queue.Queue, 数据库: 任务数据库):
        # 基础属性
        self.机器人标志 = 机器人标志
        self.消息队列 = 消息队列#用来给监控中心发送消息
        self.数据库 = 数据库


        self.暂停事件 = threading.Event()
        self.停止事件 = threading.Event()
        self.停止事件.set()#目前未启动线程,处于停止状态
        self.雷电模拟器=雷电模拟器操作类(self.数据库.获取机器人设置(机器人标志).雷电模拟器索引)
        # self.op:op类


    def 启动(self):
        if self.停止事件.is_set() :
            self.停止事件.clear()
            self.主线程 = threading.Thread(
                target=self._任务流程,
                name=f"任务线程-{self.机器人标志}",
                daemon=True
            )
            self.主线程.start()


        else:
            self._往数据库写日志("目前线程未停止,无需再次启动")

    def 请求暂停(self):
        """标记暂停状态"""
        self.暂停事件.set()


    def 请求继续(self):
        """清除暂停状态"""
        self.暂停事件.clear()


    def 请求终止(self,停止原因=""):
        """标记终止状态"""
        self.请求继续()#唤醒可能已经暂停的线程
        self.停止事件.set()

        # if hasattr(self, 'op') and self.op:
        #     self._往数据库写日志("触发终止,开始解绑释放资源,停止原因:"+停止原因)
        #     self.op.解绑()
        #     self.op = None  # 显式释放资源

        #等待线程停止
        if self.主线程.is_alive():
            self.主线程.join()

        #print("成功终止")



    def _任务流程(self):
        """主任务逻辑"""

        self.op = op类(self.雷电模拟器.取绑定窗口句柄的下级窗口句柄())
        if self.op is None:
            print("op创建失败")


        上下文=任务上下文(
            机器人标志=self.机器人标志,
            消息队列=self.消息队列,
            数据库= self.数据库,
            停止事件=self.停止事件,
            暂停事件=self.暂停事件,
            op=self.op,
            雷电模拟器=self.雷电模拟器,
            鼠标=鼠标控制器(self.雷电模拟器.取绑定窗口句柄()),
            键盘=键盘控制器(self.雷电模拟器.取绑定窗口句柄())
        )
        上下文.日志记录器("开始执行")
        try:
            尝试次数=0
            #检查图片是否可以正常获取
            for 尝试次数 in range(3):
                try:
                    图像=上下文.op.获取屏幕图像cv(0, 0, 800, 600)
                    #print(self.机器人标志,图像)
                    #print(图像)
                    # cv2.imshow('屏幕截图', 图像)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                    break
                except 图像获取失败 as 异常实例:
                    if 尝试次数<2:
                        if 尝试次数>0:
                             上下文.日志记录器("获取图像黑屏,尝试激活模拟器修复")
                        time.sleep(0.5)
                        上下文.鼠标.移动到(467, 363)
                        上下文.鼠标.左键按下()
                        for _ in range(45):
                            上下文.鼠标.移动相对位置(0, -5)
                            time.sleep(0.005)
                        上下文.鼠标.左键抬起()
                        time.sleep(1)
                        # 上下文.键盘.按字符按压("f5")
                    else:
                        #上下文.日志记录器(f"重试 {尝试次数} 次后仍失败,再次抛出异常")
                        上下文.op.安全清理()
                        raise 图像获取失败(f"重试获取图片 {尝试次数} 次后仍失败")


            上下文.日志记录器("模拟器图像获取正常")
            #self.停止事件.set()
            #上下文.延时(100)

           # 启动游戏().执行(上下文)

            上下文.op.安全清理()
            print("-"*10+F"{self.机器人标志} 线程自然消亡"+"-"*10)
            #上下文.op.解绑()

        except Exception as e:
            #异常会导致停止执行脚本,不会进一步记录日志
            #然后会被监控中心检测到无心跳，导致重启
            上下文.发送重启请求(f"异常: {str(e)}")
            #self._往数据库写日志(f"异常: {str(e)}",0)
            print("-"*10+F"{self.机器人标志} 线程因为异常而消亡"+"-"*10+f"异常: {str(e)}")
        except SystemExit as e:
            print("-"*10+F"{self.机器人标志} 线程因为捕获到退出而消亡"+"-"*10)
            print("捕获到退出：", e)




    def 检查超时(self)  -> tuple[bool, str]:
        """检查是否超时，返回 (是否超时, 原因)。未超时返回 (False, '')"""

        最后日志 = self.数据库.读取最后日志(self.机器人标志)
        # 无历史日志的情况
        if not 最后日志:
            return (False, "无历史日志记录")  # 无日志视为第一次启动,不是超时的异常状态

        # 主动停止不视为超时
        if self.停止事件.is_set():
            print(F"{self.机器人标志} 线程已主动停止,不是异常状态")
            return (False, "无历史日志记录")

        if time.time() > 最后日志.下次超时:
            实际间隔 = round(time.time() - 最后日志.记录时间)
            超时阈值 = round(最后日志.下次超时 - 最后日志.记录时间)

            原因 = (
                f"数据库最后日志记录已超时（内容：[{最后日志.日志内容}]），"
                f"实际间隔 {实际间隔} 秒超过阈值 {超时阈值} 秒"
            )
            #原因 = f"现在时间距数据库记录最后日志[{最后日志.日志内容}]已间隔{time.time()-最后日志.记录时间}，超过阈值{(最后日志.下次超时-最后日志.记录时间)}"
            return True,原因

        return (False, "")


        #return time.time() > 最后日志.下次超时 if 最后日志 else False
    #
    # def 停止(self):
    #     """停止线程"""
    #     self.已停止 = True
    #     if self.主线程.is_alive():
    #         self.主线程.join()
    #     self.状态 = "已停止"
