import queue
import tkinter as tk
from tkinter import ttk, messagebox

from 数据库.任务数据库 import 任务数据库
from 线程.自动化机器人 import 自动化机器人
from .ui_controls import 左侧控制面板
from .ui_config import 配置面板
from .ui_log import 日志面板


class 增强型机器人控制界面:
    def __init__(self, master, 监控中心):
        self.master = master
        self.监控中心 = 监控中心
        self.master.title("机器人监控控制中心 v2.0")
        self._设置窗口尺寸(1000, 700)

        self.日志队列 = self.监控中心.日志队列

        self.当前机器人ID = None
        self.上一次机器人ID = None
        self.数据库 = 任务数据库()
        self.配置缓存 = {}  # 缓存未保存的修改

        self._创建主框架()
        self._创建子组件()
        self._定时刷新()
        #self._配置现代化样式()
        self._加载保存的配置()  # 启动时自动加载
        self.master.protocol("WM_DELETE_WINDOW", self._窗口关闭处理)

    def _配置现代化样式(self):
        """配置现代化控件样式"""
        style = ttk.Style()

        # 配置圆角按钮
        style.configure("TButton", padding=6, relief="flat", font=("Segoe UI", 10))
        style.map("TButton",
                  relief=[("active", "sunken"), ("!active", "flat")],
                  background=[("active", "#e5e5e5"), ("!active", "white")]
                  )

        # 状态按钮颜色
        style.configure("success.TButton", foreground="white", background="#2ea44f")
        style.map("success.TButton",
                  background=[("active", "#22863a"), ("!active", "#2ea44f")])
        style.configure("danger.TButton", foreground="white", background="#cb2431")
        style.map("danger.TButton",
                  background=[("active", "#9f1c23"), ("!active", "#cb2431")])
        style.configure("primary.TButton", foreground="white", background="#0366d6")
        style.map("primary.TButton",
                  background=[("active", "#0256b5"), ("!active", "#0366d6")])

        # 列表样式
        style.configure("TListbox", font=("Segoe UI", 10), relief="flat")

        # 标签框样式
        style.configure("TLabelframe", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))

        # 输入控件
        style.configure("TEntry", padding=5, relief="flat")

    def _定时刷新(self):
        self.左侧控制面板.更新机器人列表()
        #self.日志面板.更新日志显示(self.获取当前机器人())

        self.master.after(500, self._定时刷新)

    def 获取当前机器人(self) -> 自动化机器人 | None:
        if self.当前机器人ID:
            return self.监控中心.机器人池.get(self.当前机器人ID)
        return None

    def _加载保存的配置(self):
        """从数据库加载已保存的配置"""
        所有配置 = self.数据库.查询所有机器人设置()
        for 机器人标志, 设置 in 所有配置.items():
            try:
                self.监控中心.创建机器人(
                    机器人标志=机器人标志,
                    初始设置=设置  # 这里设置已经是一个 机器人设置 实例
                )
            except Exception as e:
                messagebox.showerror("配置加载错误", f"加载{机器人标志}失败: {str(e)}")

    def _设置窗口尺寸(self, 宽度, 高度):
        屏幕宽度 = self.master.winfo_screenwidth()
        屏幕高度 = self.master.winfo_screenheight()
        self.master.geometry(f"{宽度}x{高度}+{(屏幕宽度 - 宽度) // 2}+{(屏幕高度 - 高度) // 2}")

    def _创建主框架(self):
        self.主框架 = ttk.Frame(self.master)
        self.主框架.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _创建子组件(self):
        # 创建左侧控制面板
        self.左侧控制面板 = 左侧控制面板(
            self.主框架,
            self.监控中心,
            self.数据库,
            self.设置当前机器人ID,
            self.获取当前机器人
        )
        self.左侧控制面板.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        # 创建右侧面板容器
        右侧容器 = ttk.Notebook(self.主框架)
        右侧容器.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # 创建日志面板
        self.日志面板 = 日志面板(右侧容器, self.日志队列)
        右侧容器.add(self.日志面板, text="运行日志")

        # 创建配置面板
        self.配置面板 = 配置面板(
            右侧容器,
            self.左侧控制面板.当前机器人ID,
            self.数据库,
            self.监控中心,
            self.左侧控制面板.更新机器人列表,
            self.日志面板.添加日志
        )
        右侧容器.add(self.配置面板, text="配置管理")

    def 设置当前机器人ID(self, 机器人ID):
        self.当前机器人ID = 机器人ID
        self.左侧控制面板.当前机器人ID = 机器人ID
        self.配置面板.当前机器人ID = 机器人ID
        self.配置面板._更新按钮状态()
        self.左侧控制面板.更新状态显示()

        # 通知日志面板切换机器人
        self.日志面板.设置当前机器人(机器人ID)



    def _窗口关闭处理(self):
        # 遍历所有机器人，停止它们
        for 机器人 in self.监控中心.机器人池.values():
            try:
                机器人.停止()
            except Exception as e:
                print(f"停止机器人 {机器人.机器人标志} 时出错: {e}")

        self.日志面板.销毁()
        self.master.destroy()