import threading
import queue
import time
from time import sleep

from 数据库.任务数据库 import 任务数据库, 用户设置
from 线程.用户任务线程 import 用户任务线程


# ==== 监控中心 ====
class 任务监控中心:
    """增强型监控服务"""

    def __init__(self):
        self.在线用户线程池 = {}
        self.消息队列 = queue.Queue()#所有在线用户共用一个消息队列和数据库
        self.数据库 = 任务数据库()
        self.运行标志 = True

        # 启动监控线程
        self.监控线程 = threading.Thread(
            target=self._监控循环,
            name="全局监控",
            daemon=True
        )
        self.监控线程.start()

    def 创建用户任务(self, 用户标识: str, 初始设置: 用户设置 = None):
        """创建新任务"""
        if 用户标识 in self.在线用户线程池:
            raise ValueError("用户已存在")

        新线程 = 用户任务线程(用户标识, self.消息队列, self.数据库)

        if 初始设置:
            self.数据库.保存用户设置(用户标识,初始设置)
        self.在线用户线程池[用户标识] = 新线程
        新线程.启动工作线程()

    def _监控循环(self):

        """监控主循环"""
        while self.运行标志:
            # 检查任务状态
            for 用户标识, 线程 in list(self.在线用户线程池.items()):
                if  线程.检查超时():
                    self.消息队列.put(f"用户{用户标识} 心跳超时，重启中...")
                    线程.停止()
                    线程.启动工作线程()

            # 处理消息
            self._处理消息()
            time.sleep(1)

    def _处理消息(self):
        """处理各个线程发过来的消息"""
        while not self.消息队列.empty():
            消息 = self.消息队列.get()
            print(f"[监控] {time.ctime()}: {消息}")
            self.消息队列.task_done()



# ==== 使用示例 ====
if __name__ == "__main__":
    # 初始化系统
    监控中心 = 任务监控中心()

    # 创建默认配置用户
    监控中心.创建用户任务("普通用户",用户设置(雷电模拟器索引=0))

    sleep(400000)
