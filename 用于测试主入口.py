import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time

from 主入口 import 机器人监控中心
from 数据库.任务数据库 import 机器人设置, 任务数据库
from 线程.自动化机器人 import 自动化机器人
from sv_ttk import set_theme  # 新增主题库

class 机器人控制界面:
    def __init__(self, master, 监控中心):
        self.master = master
        self.监控中心 = 监控中心
        self.master.title("机器人监控控制中心 v1.0")

        # 居中窗口
        self._设置窗口尺寸(宽度=1000, 高度=600)

        self.当前机器人ID = None
        self.数据库 = 任务数据库()

        self._创建主框架()
        self._创建左侧控制面板()
        self._创建右侧显示面板()
        self._定时刷新()
        #设置Win11风格主题
        set_theme("light")  # 可选"dark"暗色主题
        self._配置现代化样式()


    def _配置现代化样式(self):
        """配置现代化控件样式"""
        style = ttk.Style()

        # 配置圆角按钮
        style.configure("TButton", padding=6, relief="flat",
                        font=("Segoe UI", 10))
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
        style.configure("TCombobox", padding=5)
    def _设置窗口尺寸(self, 宽度, 高度):
        屏幕宽度 = self.master.winfo_screenwidth()
        屏幕高度 = self.master.winfo_screenheight()
        x坐标 = (屏幕宽度 - 宽度) // 2
        y坐标 = (屏幕高度 - 高度) // 2
        self.master.geometry(f"{宽度}x{高度}+{x坐标}+{y坐标}")

    def _创建主框架(self):
        self.主框架 = ttk.Frame(self.master)
        self.主框架.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _创建左侧控制面板(self):
        左侧容器 = ttk.LabelFrame(self.主框架, text="机器人控制台")
        左侧容器.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.机器人列表框 = tk.Listbox(左侧容器, width=25, height=15, selectmode=tk.SINGLE)
        self.机器人列表框.pack(pady=5, fill=tk.BOTH, expand=True)
        self.机器人列表框.bind('<<ListboxSelect>>', self.更新当前选择)

        self.当前机器人标签 = ttk.Label(左侧容器, text="当前选择：无", font=('微软雅黑', 10, 'bold'))
        self.当前机器人标签.pack(pady=5)

        控制面板 = ttk.Frame(左侧容器)
        控制面板.pack(pady=10)

        按钮配置 = [
            ('启动', 'green', self.启动机器人),
            ('暂停', 'orange', self.暂停机器人),
            ('继续', 'blue', self.继续机器人),
            ('停止', 'red', self.停止机器人)
        ]

        for i, (文字, 颜色, 回调) in enumerate(按钮配置):
            按钮 = ttk.Button(控制面板, text=文字, command=回调, style=f'{颜色}.TButton')
            按钮.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="nsew")

    def _创建右侧显示面板(self):
        右侧容器 = ttk.Frame(self.主框架)
        右侧容器.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        日志框架 = ttk.LabelFrame(右侧容器, text="实时日志")
        日志框架.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.日志文本框 = scrolledtext.ScrolledText(日志框架, wrap=tk.WORD, width=80, height=15, font=('Consolas', 9))
        self.日志文本框.pack(fill=tk.BOTH, expand=True)
        self.日志文本框.configure(state='disabled')

        配置框架 = ttk.LabelFrame(右侧容器, text="新建机器人配置")
        配置框架.pack(fill=tk.X, padx=5, pady=5)

        表单配置 = [
            ('机器人标识', 'entry', 'robot_1'),
            ('模拟器索引', 'entry', '0'),
            ('服务器', 'combo', ['国际服', '国服']),
            ('最小资源', 'entry', '200000')
        ]

        self.配置输入项 = {}
        for 行, (标签, 类型, 默认值) in enumerate(表单配置):
            ttk.Label(配置框架, text=f"{标签}：").grid(row=行, column=0, padx=5, pady=2, sticky=tk.E)

            if 类型 == 'entry':
                控件 = ttk.Entry(配置框架)
                控件.insert(0, 默认值)
            elif 类型 == 'combo':
                控件 = ttk.Combobox(配置框架, values=默认值)
                控件.current(0)

            控件.grid(row=行, column=1, padx=5, pady=2, sticky=tk.W)
            self.配置输入项[标签] = 控件

        ttk.Button(配置框架, text="创建新机器人", command=self.创建新机器人, style='green.TButton')\
            .grid(row=行 + 1, column=0, columnspan=2, pady=5)

    def _定时刷新(self):
        self.更新机器人列表()
        self.更新日志显示()
        self.master.after(1000, self._定时刷新)

    def 更新机器人列表(self):
        原选中ID = self.当前机器人ID
        原列表内容 = self.机器人列表框.get(0, tk.END)
        新列表内容 = list(self.监控中心.机器人池.keys())

        if 原列表内容 != 新列表内容:
            self.机器人列表框.delete(0, tk.END)
            for 标识 in 新列表内容:
                self.机器人列表框.insert(tk.END, 标识)

        if 原选中ID and 原选中ID in 新列表内容:
            index = 新列表内容.index(原选中ID)
            self.机器人列表框.selection_clear(0, tk.END)
            self.机器人列表框.selection_set(index)
            self.机器人列表框.activate(index)
            self.机器人列表框.see(index)

    def 更新日志显示(self):
        当前机器人 = self.获取当前机器人()

        if 当前机器人 is None:
            模拟日志 = [
                f"[{time.strftime('%H:%M:%S')}] 系统状态正常",
                f"[{time.strftime('%H:%M:%S')}] 机器人A 完成任务采集",
                f"[{time.strftime('%H:%M:%S')}] 警告：机器人B 响应超时"
            ]
        else:
            日志列表 = 当前机器人.数据库.查询日志历史(当前机器人.机器人标志)
            日志列表.sort(key=lambda 日志: 日志.记录时间)
            模拟日志 = [
                f"[{time.strftime('%H:%M:%S', time.localtime(项.记录时间))}] {项.机器人标志} {项.日志内容}"
                for 项 in 日志列表
            ]

        # 🌟 记录当前滚动条位置（0.0 ~ 1.0）
        当前视图 = self.日志文本框.yview()

        self.日志文本框.configure(state='normal')
        self.日志文本框.delete(1.0, tk.END)

        for log in 模拟日志[-500:]:
            self.日志文本框.insert(tk.END, log + '\n')

        self.日志文本框.configure(state='disabled')

        # 🌟 判断用户是否已经在底部（例如超过 0.95 就认为在底部）
        if 当前视图[1] > 0.95:
            self.日志文本框.see(tk.END)  # 自动滚动
        else:
            # 🌟 保持原来位置（注意必须在 state='normal' 后调用）
            self.日志文本框.yview_moveto(当前视图[0])

    def 更新当前选择(self, event):
        selection = self.机器人列表框.curselection()
        if selection:
            self.当前机器人ID = self.机器人列表框.get(selection[0])
            self.当前机器人标签.config(text=f"当前选择：{self.当前机器人ID}")

    def 获取当前机器人(self) -> 自动化机器人 | None:
        if self.当前机器人ID:
            return self.监控中心.机器人池.get(self.当前机器人ID)
        return None

    def 启动机器人(self):
        if robot := self.获取当前机器人():
            try:
                robot.启动()
                self.记录操作日志(f"已启动机器人 {robot.机器人标志}")
            except Exception as e:
                messagebox.showerror("操作失败", str(e))

    def 暂停机器人(self):
        if robot := self.获取当前机器人():
            robot.暂停()
            self.记录操作日志(f"已暂停机器人 {robot.机器人标志}")

    def 继续机器人(self):
        if robot := self.获取当前机器人():
            robot.继续()
            self.记录操作日志(f"已恢复机器人 {robot.机器人标志}")

    def 停止机器人(self):
        if robot := self.获取当前机器人():
            robot.停止()
            self.记录操作日志(f"已停止机器人 {robot.机器人标志}")

    def 创建新机器人(self):
        配置 = {k: v.get() for k, v in self.配置输入项.items()}

        try:
            self.监控中心.创建机器人(
                机器人标志=配置['机器人标识'],
                初始设置=机器人设置(
                    雷电模拟器索引=int(配置['模拟器索引']),
                    服务器=配置['服务器'],
                    欲进攻的最小资源=int(配置['最小资源'])
                )
            )
            self.记录操作日志(f"成功创建机器人 {配置['机器人标识']}")
            self.当前机器人ID = 配置['机器人标识']
            self.更新机器人列表()
        except ValueError as e:
            messagebox.showerror("创建失败", str(e))
        except Exception as e:
            messagebox.showerror("系统错误", str(e))

    def 记录操作日志(self, 内容):
        self.日志文本框.configure(state='normal')
        self.日志文本框.insert(tk.END, f"[操作] {内容}\n")
        self.日志文本框.configure(state='disabled')
        self.日志文本框.see(tk.END)


if __name__ == "__main__":
    监控中心 = 机器人监控中心()
    root = tk.Tk()

    # 可选：启用彩色按钮样式
    style = ttk.Style()
    # style.configure('green.TButton', foreground='white', background='#4CAF50')
    # style.configure('red.TButton', foreground='white', background='#F44336')
    # style.configure('blue.TButton', foreground='white', background='#2196F3')
    # style.configure('orange.TButton', foreground='white', background='#FF9800')

    界面 = 机器人控制界面(root, 监控中心)
    root.mainloop()
