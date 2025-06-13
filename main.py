import queue
import tkinter as tk
from ui.ui_main import 增强型机器人控制界面
from 主入口 import 机器人监控中心
from 数据库.任务数据库 import 任务数据库
from sv_ttk import set_theme

if __name__ == "__main__":
    日志队列 = queue.Queue()
    监控中心 = 机器人监控中心(日志队列)
    root = tk.Tk()
    界面 = 增强型机器人控制界面(root, 监控中心)
    set_theme("light")
    root.mainloop()