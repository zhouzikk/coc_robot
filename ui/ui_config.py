import tkinter as tk
from tkinter import ttk, messagebox

from 数据库.任务数据库 import 机器人设置


class 配置面板(ttk.Frame):
    def __init__(self, master, 当前机器人ID, 数据库, 监控中心, 更新列表回调, 记录日志回调):
        super().__init__(master)
        self.当前机器人ID = 当前机器人ID
        self.数据库 = 数据库
        self.监控中心 = 监控中心
        self.更新列表回调 = 更新列表回调
        self.记录日志回调 = 记录日志回调

        self._创建表单()
        self._创建按钮()
        self._更新按钮状态()

    def _创建表单(self):
        配置表单 = ttk.Frame(self)
        配置表单.pack(pady=10, padx=10, fill=tk.X)

        配置项定义 = [
            ('机器人标识', 'entry', 'robot_'),
            ('模拟器索引', 'spinbox', (0, 99, 1)),
            ('服务器', 'combo', ['国际服', '国服']),
            ('最小资源', 'entry', '200000'),
            ('进攻资源边缘靠近比例下限', 'entry', '0.6'),
            ('是否开启刷墙', 'combo', ['开启', '关闭']),
            ('刷墙起始金币', 'entry', '200000'),
            ('刷墙起始圣水', 'entry', '200000'),
        ]
        self.配置输入项 = {}
        for 行, (标签, 类型, 默认值) in enumerate(配置项定义):
            ttk.Label(配置表单, text=f"{标签}：").grid(row=行, column=0, padx=5, pady=5, sticky=tk.E)

            if 类型 == 'entry':
                控件 = ttk.Entry(配置表单)
                控件.insert(0, 默认值)
            elif 类型 == 'combo':
                控件 = ttk.Combobox(配置表单, values=默认值)
                控件.current(0)
            elif 类型 == 'spinbox':
                控件 = ttk.Spinbox(配置表单, from_=默认值[0], to=默认值[1], increment=默认值[2])

            控件.grid(row=行, column=1, padx=5, pady=5, sticky=tk.EW)

            self.配置输入项[标签] = 控件
            ttk.Label(配置表单, text="*" if 标签 == "机器人标识" else "").grid(row=行, column=2, sticky=tk.W)

    def _创建按钮(self):
        按钮框架 = ttk.Frame(self)
        按钮框架.pack(pady=10, fill=tk.X)

        # 状态显示标签
        self.配置状态标签 = ttk.Label(按钮框架, text="就绪", foreground="#666")
        self.配置状态标签.pack(side=tk.LEFT, padx=50)

        # 按钮容器（右对齐）
        操作按钮容器 = ttk.Frame(按钮框架)
        操作按钮容器.pack(side=tk.LEFT)

        # 动态按钮组
        self.主操作按钮 = ttk.Button(
            操作按钮容器,
            text="新建机器人",
            command=self._处理主操作
        )
        self.主操作按钮.pack(side=tk.LEFT, padx=2)

        self.次要操作按钮 = ttk.Button(
            操作按钮容器,
            text="重置表单",
            command=self._重置表单操作
        )
        self.次要操作按钮.pack(side=tk.LEFT, padx=2)

    def _更新按钮状态(self):
        """根据当前模式更新按钮状态"""
        if self.当前机器人ID is None:  # 新建模式
            self.主操作按钮.configure(text="创建新机器人")
            self.次要操作按钮.configure(text="清空表单", state=tk.NORMAL)
            self.配置状态标签.configure(text="正在创建新配置")
        else:  # 编辑模式
            self.主操作按钮.configure(text="保存修改")
            self.次要操作按钮.configure(text="放弃修改", state=tk.NORMAL)
            self.配置状态标签.configure(text=f"正在编辑：{self.当前机器人ID}")

    def _处理主操作(self):
        """智能处理保存/创建操作"""
        if self.当前机器人ID:
            self.应用更改()
        else:
            self._执行新建操作()

    def _重置表单操作(self):
        """根据模式执行不同重置操作"""
        if self.当前机器人ID:
            self.载入选中配置()  # 放弃修改
            self.配置状态标签.configure(text="已恢复原始配置", foreground="green")
        else:
            self.新建机器人()
            self.配置状态标签.configure(text="表单已重置", foreground="blue")
        self._更新按钮状态()
        self.master.after(2000, lambda: self.配置状态标签.configure(text=""))

    def _执行新建操作(self):
        try:
            self.应用更改()
            self._更新按钮状态()
            self.配置状态标签.configure(text="创建成功！", foreground="darkgreen")
        except Exception as e:
            self.配置状态标签.configure(text=f"创建失败：{str(e)}", foreground="red")
        finally:
            self.master.after(2000, self._更新按钮状态)

    def 新建机器人(self):
        """清空表单准备新建"""
        for 标签, 控件 in self.配置输入项.items():
            if 标签 == "机器人标识":
                控件.delete(0, tk.END)
                控件.insert(0, "robot_")
            elif 标签 == "模拟器索引":
                控件.delete(0, tk.END)
                控件.insert(0, "0")
            elif 标签 == "服务器":
                控件.current(0)
            elif 标签 == "最小资源":
                控件.delete(0, tk.END)
                控件.insert(0, "200000")

    def 应用更改(self):
        配置数据 = {k: v.get() for k, v in self.配置输入项.items()}
        if not 配置数据["机器人标识"].strip():
            messagebox.showerror("错误", "机器人标识不能为空！")
            return

        try:
            新配置 = 机器人设置(
                雷电模拟器索引=int(配置数据["模拟器索引"]),
                服务器=配置数据["服务器"],
                欲进攻的最小资源=int(配置数据["最小资源"]),
                开启刷墙=True if 配置数据["是否开启刷墙"] == "开启" else False,
                刷墙起始金币=int(配置数据["刷墙起始金币"]),
                刷墙起始圣水=int(配置数据["刷墙起始圣水"]),
                欲进攻资源建筑靠近地图边缘最小比例=float(配置数据["进攻资源边缘靠近比例下限"])
            )
        except ValueError as e:
            messagebox.showerror("配置错误", f"数值格式错误: {str(e)}")
            return

        # 判断是新建还是更新
        if self.当前机器人ID is None:
            self._创建新机器人(配置数据["机器人标识"], 新配置)
        else:
            self._更新机器人配置(配置数据["机器人标识"], 新配置)
        self._更新按钮状态()

    def _创建新机器人(self, 标识, 配置):
        if 标识 in self.监控中心.机器人池:
            messagebox.showerror("错误", "该标识已存在！")
            return

        try:
            self.监控中心.创建机器人(机器人标志=标识, 初始设置=配置)
            self.数据库.保存机器人设置(标识, 配置)
            self.更新列表回调()
            self.记录日志回调(f"已创建并保存新配置：{标识}")
        except Exception as e:
            messagebox.showerror("创建失败", str(e))

    def _更新机器人配置(self, 新标识, 新配置):
        原标识 = self.当前机器人ID
        if 新标识 != 原标识 and 新标识 in self.监控中心.机器人池:
            messagebox.showerror("错误", "目标标识已存在！")
            return

        try:
            # 先停止原有机器人
            if robot := self.监控中心.机器人池.get(原标识):
                robot.停止()

            # 更新配置并保存
            self.数据库.保存机器人设置(原标识, 新配置)
            self.更新列表回调()
            self.记录日志回调(f"已更新配置：{原标识} → {新标识}")
        except Exception as e:
            messagebox.showerror("更新失败", str(e))

    def 载入选中配置(self):
        if not self.当前机器人ID:
            return

        if 配置 := self.数据库.获取机器人设置(self.当前机器人ID):
            self.配置输入项["机器人标识"].delete(0, tk.END)
            self.配置输入项["机器人标识"].insert(0, self.当前机器人ID)

            self.配置输入项["模拟器索引"].delete(0, tk.END)
            self.配置输入项["模拟器索引"].insert(0, str(配置.雷电模拟器索引))

            self.配置输入项["服务器"].set(配置.服务器)

            self.配置输入项["最小资源"].delete(0, tk.END)
            self.配置输入项["最小资源"].insert(0, str(配置.欲进攻的最小资源))

            self.配置输入项["进攻资源边缘靠近比例下限"].delete(0, tk.END)
            self.配置输入项["进攻资源边缘靠近比例下限"].insert(0, str(配置.欲进攻资源建筑靠近地图边缘最小比例))

            self.配置输入项["是否开启刷墙"].set("开启" if 配置.开启刷墙 == True else "关闭")

            self.配置输入项["刷墙起始金币"].delete(0, tk.END)
            self.配置输入项["刷墙起始金币"].insert(0, str(配置.刷墙起始金币))

            self.配置输入项["刷墙起始圣水"].delete(0, tk.END)
            self.配置输入项["刷墙起始圣水"].insert(0, str(配置.刷墙起始圣水))
            self._更新按钮状态()