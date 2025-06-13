import tkinter as tk
from tkinter import ttk, Listbox, Scrollbar
import time
from queue import Queue, Empty
import threading
from collections import defaultdict


class 日志面板(ttk.Frame):
    def __init__(self, master, 日志队列):
        super().__init__(master)
        self.日志队列 = 日志队列
        self.当前机器人ID = None
        self.日志缓存 = defaultdict(list)  # 存储所有机器人的日志
        self.最大日志条数 = 500
        self.自动滚动 = True
        self.运行标志 = True

        self._创建列表框()
        self._启动日志处理线程()

        # 初始化显示欢迎信息
        欢迎信息 = [
            f"[{time.strftime('%H:%M:%S')}] 系统状态正常",
            f"[{time.strftime('%H:%M:%S')}] 欢迎使用脚本，具体使用步骤如下:",
            f"[{time.strftime('%H:%M:%S')}] 1.在模拟器中安装部落冲突并登录你的账号，确保进入主世界。",
            f"[{time.strftime('%H:%M:%S')}] 2.模拟器分辨率设置宽800，高600，dpi160",
            f"[{time.strftime('%H:%M:%S')}] 3.部落冲突中设置配兵,目前支持所有普通兵种,超级兵种支持超级野蛮人以及超级哥布林",
            f"[{time.strftime('%H:%M:%S')}] 4.打开游戏后",
            f"[{time.strftime('%H:%M:%S')}] 5.先在左边选中需要启动的账号,点击'启动'按钮运行脚本"
        ]
        for log in 欢迎信息:
            self._安全添加日志(log, '系统')

    def _创建列表框(self):
        """创建Listbox及其滚动条"""
        # 创建框架容器
        容器 = ttk.Frame(self)
        容器.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 创建垂直滚动条
        垂直滚动条 = Scrollbar(容器)
        垂直滚动条.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建水平滚动条
        水平滚动条 = Scrollbar(容器, orient='horizontal')
        水平滚动条.pack(side=tk.BOTTOM, fill=tk.X)

        # 创建Listbox
        self.日志列表框 = Listbox(
            容器,
            yscrollcommand=垂直滚动条.set,
            xscrollcommand=水平滚动条.set,
            font=('Consolas', 9),
            bg='white',
            selectbackground='#e0e0e0',
            selectmode=tk.SINGLE,
            borderwidth=0,
            highlightthickness=0
        )
        self.日志列表框.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 配置滚动条
        垂直滚动条.config(command=self.日志列表框.yview)
        水平滚动条.config(command=self.日志列表框.xview)

        # 添加右键菜单
        self._添加右键菜单()

    def _添加右键菜单(self):
        """为Listbox添加右键菜单"""
        self.右键菜单 = tk.Menu(self, tearoff=0)
        self.右键菜单.add_command(label="复制选中行", command=self._复制选中行)
        self.右键菜单.add_command(label="清空当前日志", command=self._清空当前日志)
        self.右键菜单.add_separator()
        self.右键菜单.add_command(label="自动滚动", command=self._切换自动滚动)

        # 绑定右键事件
        self.日志列表框.bind("<Button-3>", self._显示右键菜单)

        # 初始化自动滚动状态
        self.自动滚动 = True

    def _显示右键菜单(self, event):
        """显示右键菜单"""
        self.右键菜单.post(event.x_root, event.y_root)

    def _复制选中行(self):
        """复制选中行到剪贴板"""
        选中行 = self.日志列表框.curselection()
        if 选中行:
            内容 = self.日志列表框.get(选中行[0])
            self.clipboard_clear()
            self.clipboard_append(内容)

    def _清空当前日志(self):
        """清空当前显示的日志（不删除缓存）"""
        self.日志列表框.delete(0, tk.END)
        if self.当前机器人ID:
            # 保留缓存，只清空显示
            for log in self.日志缓存[self.当前机器人ID]:
                self.日志列表框.insert(tk.END, log)
            if self.自动滚动:
                self.日志列表框.see(tk.END)

    def _切换自动滚动(self):
        """切换自动滚动状态"""
        self.自动滚动 = not self.自动滚动
        if self.自动滚动:
            self.日志列表框.see(tk.END)

    def _安全添加日志(self, 日志内容, 机器人ID):
        """线程安全地添加日志到列表框和缓存"""
        # 添加到缓存
        if 机器人ID not in self.日志缓存:
            self.日志缓存[机器人ID] = []

        self.日志缓存[机器人ID].append(日志内容)

        # 如果缓存超过最大限制，移除最旧的日志
        if len(self.日志缓存[机器人ID]) > self.最大日志条数:
            self.日志缓存[机器人ID].pop(0)

        # 如果是当前显示的机器人，添加到列表框中
        if 机器人ID == self.当前机器人ID or 机器人ID == '系统':
            self.日志列表框.insert(tk.END, 日志内容)

            # 如果列表框中日志超过最大限制，移除最旧的日志
            if self.日志列表框.size() > self.最大日志条数:
                self.日志列表框.delete(0)

            if self.自动滚动:
                self.日志列表框.see(tk.END)
        # elif self.当前机器人ID==None:
        #     self.日志列表框.insert(tk.END, "日志内容")

    def _启动日志处理线程(self):
        """启动后台线程处理日志队列"""
        self.日志处理线程 = threading.Thread(
            target=self._处理日志队列,
            daemon=True
        )
        self.日志处理线程.start()

    def _处理日志队列(self):
        """处理日志队列中的消息"""
        while self.运行标志:
            try:
                # 从队列获取消息，最多等待100ms
                日志消息 = self.日志队列.get(timeout=0.1)
                if 日志消息:
                    # 使用after方法安全更新UI
                    self.after(0, self._处理单条日志, 日志消息)
            except Empty:
                # 队列为空，继续等待
                continue
            except Exception as e:
                print(f"日志处理错误: {e}")

    def _处理单条日志(self, 日志消息):
        """处理单条日志消息"""
        内容 = 日志消息.get('内容', '')
        机器人ID = 日志消息.get('机器人ID', '系统')
        类型 = 日志消息.get('类型', '运行')

        self._安全添加日志(内容, 机器人ID)

    def 设置当前机器人(self, 机器人ID):
        """设置当前显示的机器人"""
        # 保存当前滚动位置
        当前视图 = self.日志列表框.yview()

        # 清空当前显示
        self.日志列表框.delete(0, tk.END)

        # 更新当前机器人ID
        self.当前机器人ID = 机器人ID

        # 显示新机器人的日志
        if 机器人ID in self.日志缓存:
            for log in self.日志缓存[机器人ID]:
                self.日志列表框.insert(tk.END, log)
        else:
            self.日志缓存[机器人ID] = []
            self.日志列表框.insert(
                tk.END,
                f"[{time.strftime('%H:%M:%S')}] 开始显示机器人 {机器人ID} 的日志"
            )

        # 恢复滚动位置或滚动到底部
        if 当前视图[1] >= 0.99:  # 如果之前已经滚动到底部
            self.日志列表框.see(tk.END)
        else:
            # 计算并恢复原来的滚动位置
            总行数 = self.日志列表框.size()
            if 总行数 > 0:
                目标位置 = int(当前视图[0] * 总行数)
                if 目标位置 < 总行数:
                    self.日志列表框.yview(目标位置)

    def 添加日志(self, 内容, 机器人ID=None, 类型='运行'):
        """添加日志到队列"""
        self.日志队列.put({
            '内容': 内容,
            '机器人ID': 机器人ID,
            '类型': 类型
        })

    def 销毁(self):
        """清理资源"""
        self.运行标志 = False
        if self.日志处理线程.is_alive():
            self.日志处理线程.join(timeout=1.0)