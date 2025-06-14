import tkinter as tk
from tkinter import simpledialog, messagebox

from sv_ttk import set_theme


class 任务调度器界面:
    def __init__(self, 根窗口):
        self.根 = 根窗口
        self.根.title("任务调度器")
        self.任务列表 = []

        self.任务高度 = 50
        self.任务间距 = 6
        self.拖动索引 = None
        self.占位位置 = None
        self.拖动浮动框 = None
        self.占位框 = None
        self.偏移x = 0  # 新增：存储鼠标在任务内部的X偏移
        self.偏移y = 0  # 新增：存储鼠标在任务内部的Y偏移

        self.添加按钮 = tk.Button(self.根, text="添加任务", command=self.添加任务)
        self.添加按钮.pack(pady=10)

        self.任务框架 = tk.Frame(self.根)
        self.任务框架.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.刷新任务显示()
        set_theme("light")

    def 添加任务(self):
        任务名 = simpledialog.askstring("添加任务", "请输入任务名称：")
        if not 任务名:
            return
        新任务 = {
            "名称": 任务名,
            "参数": {
                "执行时间": "12:00",
                "优先级": 1
            }
        }
        self.任务列表.append(新任务)
        self.刷新任务显示()

    def 刷新任务显示(self):
        for 小部件 in self.任务框架.winfo_children():
            小部件.destroy()

        for 索引, 任务 in enumerate(self.任务列表):
            外框 = tk.Frame(self.任务框架, bd=2, relief=tk.RIDGE, height=self.任务高度)
            外框.pack(fill=tk.X, pady=self.任务间距)
            外框.pack_propagate(False)

            标签 = tk.Label(外框, text=f"{索引 + 1}. {任务['名称']}", anchor="w", bg="#eef", height=2)
            标签.pack(fill=tk.BOTH, expand=True)

            标签.bind("<Button-1>", lambda e, i=索引: self.开始拖动(e, i))
            标签.bind("<B1-Motion>", self.执行拖动)
            标签.bind("<ButtonRelease-1>", self.结束拖动)

            外框.bind("<Button-3>", lambda e, i=索引: self.显示右键菜单(e, i))
            标签.bind("<Button-3>", lambda e, i=索引: self.显示右键菜单(e, i))

    def 显示右键菜单(self, 事件, 索引):
        菜单 = tk.Menu(self.根, tearoff=0)
        菜单.add_command(label="编辑参数", command=lambda: self.编辑参数(索引))
        菜单.post(事件.x_root, 事件.y_root)

    def 编辑参数(self, 索引):
        任务 = self.任务列表[索引]
        参数 = 任务["参数"]
        新执行时间 = simpledialog.askstring("编辑参数", "请输入执行时间：", initialvalue=参数["执行时间"])
        新优先级 = simpledialog.askinteger("编辑参数", "请输入优先级（数字）：", initialvalue=参数["优先级"])
        if 新执行时间 and 新优先级 is not None:
            参数["执行时间"] = 新执行时间
            参数["优先级"] = 新优先级
            messagebox.showinfo("成功", "参数已更新！")

    def 开始拖动(self, 事件, 索引):
        self.拖动索引 = 索引
        self.占位位置 = 索引
        # 保存鼠标在任务内部的偏移量
        self.偏移x = 事件.x
        self.偏移y = 事件.y

        原任务框 = self.任务框架.winfo_children()[索引]
        x = 原任务框.winfo_rootx()
        y = 原任务框.winfo_rooty()
        w = 原任务框.winfo_width()
        h = 原任务框.winfo_height()

        self.拖动浮动框 = tk.Toplevel(self.根)
        self.拖动浮动框.overrideredirect(True)
        self.拖动浮动框.geometry(f"{w}x{h}+{x}+{y}")
        tk.Label(self.拖动浮动框, text=self.任务列表[索引]['名称'], bg="lightblue", anchor="w").pack(fill=tk.BOTH,
                                                                                                     expand=True)

        self.占位框 = tk.Frame(self.任务框架, height=h, bg="#ccc")
        原任务框.pack_forget()
        self.占位框.pack(fill=tk.X, pady=self.任务间距)
        self.任务框架.update_idletasks()

    def 执行拖动(self, 事件):
        if not self.拖动浮动框:
            return

        # 使用鼠标偏移量计算浮动框位置
        x = 事件.x_root - self.偏移x
        y = 事件.y_root - self.偏移y
        self.拖动浮动框.geometry(f"+{x}+{y}")

        鼠标y = 事件.y_root - self.任务框架.winfo_rooty()
        # 计算每个任务区域的总高度（任务高度+2倍间距）
        区域高度 = self.任务高度 + 2 * self.任务间距
        新索引 = 鼠标y // 区域高度
        新索引 = max(0, min(len(self.任务列表) - 1, 新索引))  # 确保索引在有效范围内

        if self.占位框 and self.占位框.winfo_exists():
            self.占位框.pack_forget()
            当前子部件 = self.任务框架.pack_slaves()  # 获取当前所有打包的部件

            # 正确处理边界情况
            if 新索引 >= len(当前子部件):
                self.占位框.pack(fill=tk.X, pady=self.任务间距)
            else:
                self.占位框.pack(before=当前子部件[新索引], fill=tk.X, pady=self.任务间距)

        self.占位位置 = 新索引

    def 结束拖动(self, 事件=None):
        if self.拖动浮动框:
            self.拖动浮动框.destroy()
            self.拖动浮动框 = None
        if self.占位框:
            self.占位框.destroy()
            self.占位框 = None

        if self.拖动索引 is not None and self.占位位置 is not None and self.拖动索引 != self.占位位置:
            移动任务 = self.任务列表.pop(self.拖动索引)
            # 调整插入位置：如果目标位置在原位置之后，需要减1
            if self.占位位置 > self.拖动索引:
                self.任务列表.insert(self.占位位置 - 1, 移动任务)
            else:
                self.任务列表.insert(self.占位位置, 移动任务)

        self.拖动索引 = None
        self.占位位置 = None
        self.刷新任务显示()


if __name__ == "__main__":

    根 = tk.Tk()

    界面 = 任务调度器界面(根)

    根.mainloop()