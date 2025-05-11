import threading
import queue
import time
from time import sleep

from 数据库.任务数据库 import 任务数据库, 机器人设置
from 线程.自动化机器人 import 自动化机器人


# ==== 监控中心 ====
class 机器人监控中心:
    """增强型监控服务"""

    def __init__(self):
        self.机器人池 = {}
        self.全局消息队列 = queue.Queue()#所有在线用户共用一个消息队列和数据库
        self.数据库 = 任务数据库()
        self.运行标志 = True

        # 启动监控线程,监控每一个机器人的行为
        self.监控线程 = threading.Thread(
            target=self._监控循环,
            name="机器人监控线程",
            daemon=True
        )
        self.监控线程.start()

    def 创建并启动机器人(self, 机器人标志: str, 初始设置: 机器人设置 = None):
        """创建机器人并启动"""
        if 机器人标志 in self.机器人池:
            raise ValueError(f"机器人标志[{机器人标志}],已存在")
        else:
            机器人实例 = 自动化机器人(机器人标志, self.全局消息队列, self.数据库)

        if 初始设置:
            self.数据库.保存机器人设置(机器人标志, 初始设置)

        self.机器人池[机器人标志] = 机器人实例
        机器人实例.启动()

    def _监控循环(self):
        """持续监控所有机器人的状态"""
        while self.运行标志:
            # 检查任务状态
            for 用户标识, 线程 in list(self.机器人池.items()):
                print("监控中")
                if  线程.检查超时():

                    self.全局消息队列.put(f"机器人{用户标识} 心跳超时，开始停止,并释放资源...")
                    # 线程.请求终止()
                    # 线程.启动()
                    # 先移出机器人池再终止
                    del self.机器人池[用户标识]
                    线程.请求终止("无心跳")
                    # 等待模拟器冷却
                    time.sleep(2)  # 关键：给模拟器恢复时间
                    # 完全新建实例避免状态污染
                    self.创建并启动机器人(用户标识)
                    self.全局消息队列.put(f"机器人{用户标识} 已停止完毕,现在重启")

                # 处理消息
            self._处理消息()
            time.sleep(1)

    def _处理消息(self):
        """处理来自各个机器人的消息"""
        while not self.全局消息队列.empty():
            消息 = self.全局消息队列.get()
            if isinstance(消息, dict) and 消息.get("类型") == "重启请求":
                self.处理重启请求(消息["机器人标志"], 消息.get("原因", ""))
            else:
                print(f"[监控中心消息] {time.ctime()}: {消息}")
            self.全局消息队列.task_done()

    def 处理重启请求(self, 机器人标志: str, 重启原因: str):
        """处理机器人发起的重启请求"""
        self.全局消息队列.put(f"机器人 {机器人标志} 请求重启，原因：{重启原因}")
        if 机器人标志 in self.机器人池:
            机器人实例 = self.机器人池[机器人标志]
            # 终止当前实例
            机器人实例.请求终止(重启原因)
            # 等待线程结束
            if 机器人实例.主线程.is_alive():
                机器人实例.主线程.join()
            # 移除旧实例
            del self.机器人池[机器人标志]
            # 等待模拟器冷却
            time.sleep(2)
            # 创建新实例并启动
            self.创建并启动机器人(机器人标志)
            self.全局消息队列.put(f"机器人 {机器人标志} 重启完成")


# ==== 使用示例 ====
if __name__ == "__main__":
    # 初始化系统
    机器人监控系统 = 机器人监控中心()

    # 创建默认配置用户
    机器人监控系统.创建并启动机器人("模拟器索引0", 机器人设置(雷电模拟器索引=0))
    #监控中心.创建用户任务("模拟器索引1",用户设置(雷电模拟器索引=1))
    sleep(400000)
