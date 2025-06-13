import tkinter as tk
from tkinter import ttk, messagebox
import time


class 左侧控制面板(ttk.LabelFrame):
    def __init__(self, master, 监控中心, 数据库, 设置当前机器人ID回调, 获取当前机器人回调):
        super().__init__(master, text="机器人管理")
        self.监控中心 = 监控中心
        self.数据库 = 数据库
        self.设置当前机器人ID回调 = 设置当前机器人ID回调
        self.获取当前机器人回调 = 获取当前机器人回调
        self.当前机器人ID = None

        self._创建组件()
        self.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _创建组件(self):
        # 机器人列表管理
        self.机器人列表框 = ttk.Treeview(self, columns=('status'), show='tree headings', height=15)
        self.机器人列表框.column('#0', width=250, anchor=tk.W)
        self.机器人列表框.heading('#0', text='机器人标识', anchor=tk.W)
        self.机器人列表框.column('status', width=80, anchor=tk.CENTER)
        self.机器人列表框.heading('status', text='状态', anchor=tk.CENTER)
        self.机器人列表框.pack(pady=5, fill=tk.BOTH, expand=True)
        self.机器人列表框.bind('<<TreeviewSelect>>', self.更新当前选择)
        self.机器人列表框.bind("<Button-1>", self.处理列表点击)

        # 列表操作按钮
        列表操作面板 = ttk.Frame(self)
        列表操作面板.pack(pady=5, fill=tk.X)
        ttk.Button(列表操作面板, text="刷新列表", command=self.更新机器人列表).pack(side=tk.LEFT, padx=2)
        ttk.Button(列表操作面板, text="删除选中", command=self.删除选中机器人).pack(side=tk.LEFT, padx=2)

        # 状态显示
        self.当前状态面板 = ttk.LabelFrame(self, text="当前状态")
        self.当前状态面板.pack(fill=tk.X, pady=5)
        self.状态标签组 = {
            '标识': ttk.Label(self.当前状态面板, text="标识：-"),
            '状态': ttk.Label(self.当前状态面板, text="状态：未选择"),
            '服务器': ttk.Label(self.当前状态面板, text="服务器：-"),
            '模拟器': ttk.Label(self.当前状态面板, text="模拟器：-"),
            '资源': ttk.Label(self.当前状态面板, text="最小资源：-")
        }
        for idx, 标签 in enumerate(self.状态标签组.values()):
            标签.grid(row=idx // 2, column=idx % 2, sticky=tk.W, padx=5, pady=2)

        # 控制按钮
        控制按钮框架 = ttk.LabelFrame(self, text="控制当前选中")
        控制按钮框架.pack(fill=tk.X, pady=5)
        ttk.Button(控制按钮框架, text="启动", command=self.启动机器人).pack(side=tk.LEFT, padx=5)
        ttk.Button(控制按钮框架, text="暂停", command=self.暂停机器人).pack(side=tk.LEFT, padx=5)
        ttk.Button(控制按钮框架, text="继续", command=self.继续机器人).pack(side=tk.LEFT, padx=5)
        ttk.Button(控制按钮框架, text="停止", command=self.停止机器人).pack(side=tk.LEFT, padx=5)

    def 处理列表点击(self, event):
        """处理列表点击事件以实现取消选择"""

        item = self.机器人列表框.identify_row(event.y)

        if not item:  # 点击空白处
            self.机器人列表框.selection_remove(self.机器人列表框.selection())
            self.设置当前机器人ID回调(None)
            self.更新状态显示()
            print("点击了空白")

    def 启动机器人(self):
        机器人 = self.获取当前机器人回调()
        if 机器人:
            try:
                机器人.启动()
            except Exception as e:
                messagebox.showerror("启动失败", str(e))

    def 暂停机器人(self):
        机器人 = self.获取当前机器人回调()
        if 机器人:
            try:
                机器人.暂停()
            except Exception as e:
                messagebox.showerror("暂停失败", str(e))

    def 继续机器人(self):
        机器人 = self.获取当前机器人回调()
        if 机器人:
            try:
                机器人.继续()
            except Exception as e:
                messagebox.showerror("继续失败", str(e))

    def 停止机器人(self):
        机器人 = self.获取当前机器人回调()
        if 机器人:
            try:
                机器人.停止()
            except Exception as e:
                messagebox.showerror("停止失败", str(e))

    def 删除选中机器人(self):
        if not self.当前机器人ID:
            return

        if not messagebox.askyesno("确认删除", f"确定要永久删除 {self.当前机器人ID} 的配置吗？"):
            return

        try:
            # 判断机器人是否在机器人池中
            if self.当前机器人ID in self.监控中心.机器人池:
                try:
                    # 停止机器人并移除
                    机器人实例 = self.监控中心.机器人池[self.当前机器人ID]
                    机器人实例.停止()
                    del self.监控中心.机器人池[self.当前机器人ID]
                except Exception as e:
                    messagebox.showwarning("停止失败", f"停止机器人时发生错误：{e}")

            # 删除数据库配置
            self.数据库.删除机器人设置(self.当前机器人ID)

            # 清除当前选择并刷新列表
            self.设置当前机器人ID回调(None)
            self.更新机器人列表()

        except Exception as e:
            messagebox.showerror("删除失败", f"删除过程中发生异常：{e}")

    def 更新当前选择(self, event):

        选中项 = self.机器人列表框.selection()
        if 选中项:
            新机器人ID = self.机器人列表框.item(选中项[0], 'text')
            if 新机器人ID != self.当前机器人ID:
                self.设置当前机器人ID回调(新机器人ID)
                self.更新状态显示()

    def 更新状态显示(self):
        robot = self.获取当前机器人回调()
        if robot:
            self.状态标签组['标识'].config(text=f"标识：{robot.机器人标志}")
            self.状态标签组['状态'].config(text=f"状态：{robot.当前状态}")
            self.状态标签组['服务器'].config(text=f"服务器：{robot.设置.服务器}")
            self.状态标签组['模拟器'].config(text=f"模拟器：{robot.设置.雷电模拟器索引}")
            self.状态标签组['资源'].config(text=f"最小资源：{robot.设置.欲进攻的最小资源}")
        else:
            self.状态标签组['标识'].config(text="标识：-")
            self.状态标签组['状态'].config(text="状态：未选择")
            self.状态标签组['服务器'].config(text="服务器：-")
            self.状态标签组['模拟器'].config(text="模拟器：-")
            self.状态标签组['资源'].config(text="最小资源：-")

    def 更新机器人列表(self):
        当前选择 = self.机器人列表框.selection()
        原列表项 = {self.机器人列表框.item(item, 'text'): item
                    for item in self.机器人列表框.get_children()}

        # 同步监控中心的机器人
        for 标识 in self.监控中心.机器人池.keys():
            if 标识 not in 原列表项:
                self.机器人列表框.insert('', tk.END, text=标识, values=('未运行',))

        # 移除不存在的项
        for 标识, item in 原列表项.items():
            if 标识 not in self.监控中心.机器人池:
                self.机器人列表框.delete(item)

        # 更新状态显示
        for item in self.机器人列表框.get_children():
            标识 = self.机器人列表框.item(item, 'text')
            if robot := self.监控中心.机器人池.get(标识):
                self.机器人列表框.set(item, 'status', robot.当前状态)

        # 恢复选择
        if self.当前机器人ID and self.当前机器人ID in self.监控中心.机器人池:
            for item in self.机器人列表框.get_children():
                if self.机器人列表框.item(item, 'text') == self.当前机器人ID:
                    self.机器人列表框.selection_set(item)
                    break

        # # 清除无效选择
        # if self.当前机器人ID and self.当前机器人ID not in self.监控中心.机器人池:
        #     self.设置当前机器人ID回调(None)

        # 重新设置选择（如果有当前ID）
        if self.当前机器人ID:
            for item in self.机器人列表框.get_children():
                if self.机器人列表框.item(item, 'text') == self.当前机器人ID:
                    self.机器人列表框.selection_set(item)
                    break