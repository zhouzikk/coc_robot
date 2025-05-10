import time
import threading
from abc import ABC, abstractmethod


class 可暂停任务(ABC):
    """支持实时暂停检测的任务基类"""

    def __init__(self):
        self._暂停事件 = threading.Event()  # 暂停状态标志
        self._恢复事件 = threading.Event()  # 恢复信号
        self._终止标志 = False  # 终止任务标志

    def 安全延时(self, 时长: float, 间隔=0.1):
        """可中断的延时函数"""
        剩余时间 = 时长
        while 剩余时间 > 0 and not self._终止标志:
            if self._暂停事件.is_set():
                # 进入暂停等待状态
                self._恢复事件.clear()
                self._恢复事件.wait()

            # 计算单次等待时间
            单次等待 = min(间隔, 剩余时间)
            time.sleep(单次等待)
            剩余时间 -= 单次等待

    def 暂停(self):
        """立即暂停任务"""
        self._暂停事件.set()

    def 恢复(self):
        """继续执行任务"""
        self._暂停事件.clear()
        self._恢复事件.set()

    def 终止(self):
        """彻底终止任务"""
        self._终止标志 = True
        self.恢复()  # 确保唤醒等待

    @abstractmethod
    def 执行任务(self):
        """需要实现的具体任务逻辑"""
        pass


class 复杂任务示例(可暂停任务):
    """演示包含多个延时阶段的任务"""

    def 执行任务(self):
        # 阶段一：初始化
        print("正在初始化...")
        self.安全延时(3)  # 3秒初始化

        # 阶段二：数据处理
        for i in range(1, 6):
            if self._终止标志:
                return
            print(f"处理进度 {i}/5")
            self.安全延时(1)  # 每个步骤1秒

        # 阶段三：最终确认
        print("正在保存结果...")
        self.安全延时(2)


# ==== 使用示例 ====
if __name__ == "__main__":
    任务 = 复杂任务示例()


    # 创建控制线程
    def 任务线程():
        任务.执行任务()
        print("任务执行完成" if not 任务._终止标志 else "任务已终止")


    线程 = threading.Thread(target=任务线程)
    线程.start()

    # 模拟用户操作
    time.sleep(2.5)
    print("\n用户点击暂停")
    任务.暂停()  # 此时任务处于初始化阶段最后0.5秒

    time.sleep(2)
    print("用户点击继续")
    任务.恢复()  # 恢复后继续执行

    time.sleep(3)
    print("\n用户再次暂停")
    任务.暂停()  # 暂停在数据处理阶段

    time.sleep(1)
    print("用户选择终止")
    任务.终止()

    线程.join()