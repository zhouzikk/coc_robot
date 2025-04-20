import threading
import time
import sqlite3
import queue
import json
from dataclasses import dataclass
from typing import Dict, Any

import sqlite3
import time
import json
from dataclasses import dataclass
from typing import Dict, Any, List


# ==== 数据结构 ====
@dataclass
class 任务日志:
    用户标识: str
    日志内容: str
    记录时间: float
    下次超时: float


@dataclass
class 用户设置:
    心跳间隔: float = 5.0
    最大重试次数: int = 3
    任务参数: Dict[str, Any] = None

    def __post_init__(self):
        if self.任务参数 is None:
            self.任务参数 = {}

# ==== 数据库管理 ====
class 任务数据库:
    """集成化数据库管理"""

    def __init__(self, 文件路径="任务系统.db"):
        self.文件路径 = 文件路径
        self._初始化表结构()

    def _获取连接(self):
        """获取线程安全连接"""
        conn = sqlite3.connect(
            self.文件路径,
            check_same_thread=False,
            timeout=15
        )
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _初始化表结构(self):
        """初始化所有数据库表"""
        with self._获取连接() as conn:
            # 任务日志表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS 任务日志 (
                    记录ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    用户标识 TEXT NOT NULL,
                    日志内容 TEXT,
                    记录时间 REAL NOT NULL,
                    下次超时 REAL NOT NULL
                )""")

            # 任务状态表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS 任务状态 (
                    用户标识 TEXT PRIMARY KEY,
                    进度 INTEGER DEFAULT 0,
                    附加数据 TEXT,
                    最后日志ID INTEGER
                )""")

            # 用户设置表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS 用户设置 (
                    用户标识 TEXT PRIMARY KEY,
                    设置JSON TEXT
                )""")

            # 运行数据表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS 运行数据 (
                    用户标识 TEXT PRIMARY KEY,
                    当前任务 TEXT,
                    上次更新时间 REAL,
                    状态 TEXT
                )""")

    # ==== 日志操作 ====
    def 记录日志(self, 用户标识: str, 日志内容: str, 下次超时: float):
        """原子化日志记录"""
        with self._获取连接() as conn:
            游标 = conn.execute(
                "INSERT INTO 任务日志 (用户标识, 日志内容, 记录时间, 下次超时) VALUES (?, ?, ?, ?)",
                (用户标识, 日志内容, time.time(), 下次超时)
            )
            conn.execute(
                "UPDATE 任务状态 SET 最后日志ID = ? WHERE 用户标识 = ?",
                (游标.lastrowid, 用户标识)
            )
            conn.commit()

    def 读取最后日志(self, 用户标识: str) -> 任务日志:
        """获取最后有效日志"""
        with self._获取连接() as conn:
            结果 = conn.execute("""
                SELECT 日志内容, 记录时间, 下次超时 
                FROM 任务日志 
                WHERE 用户标识 = ?
                ORDER BY 记录ID DESC 
                LIMIT 1
            """, (用户标识,)).fetchone()
        return 任务日志(用户标识, *结果) if 结果 else None

    def 查询日志历史(self, 用户标识: str, 起始时间: float = 0, 截止时间: float = None, 最大条数: int = 100) -> List[任务日志]:
        """查询用户的历史日志（可指定时间范围与返回数量）"""
        if 截止时间 is None:
            截止时间 = time.time()
        with self._获取连接() as conn:
            结果列表 = conn.execute("""
                SELECT 日志内容, 记录时间, 下次超时
                FROM 任务日志
                WHERE 用户标识 = ? AND 记录时间 BETWEEN ? AND ?
                ORDER BY 记录时间 DESC
                LIMIT ?
            """, (用户标识, 起始时间, 截止时间, 最大条数)).fetchall()
        return [任务日志(用户标识, *行) for 行 in 结果列表]

    # ==== 设置管理 ====
    def 保存用户设置(self, 用户标识: str, 设置: 用户设置):
        """保存用户配置"""
        with self._获取连接() as conn:
            conn.execute(
                "INSERT INTO 用户设置 VALUES (?, ?) ON CONFLICT DO UPDATE SET 设置JSON=excluded.设置JSON",
                (用户标识, json.dumps(设置.__dict__))
            )
            conn.commit()

    def 获取用户设置(self, 用户标识: str) -> 用户设置:
        """加载用户配置"""
        with self._获取连接() as conn:
            结果 = conn.execute(
                "SELECT 设置JSON FROM 用户设置 WHERE 用户标识 = ?",
                (用户标识,)
            ).fetchone()
        return 用户设置(**json.loads(结果[0])) if 结果 else 用户设置()

    # ==== 运行数据 ====
    def 更新运行数据(self, 用户标识: str, 当前任务: str, 状态: str):
        """更新运行时状态"""
        with self._获取连接() as conn:
            conn.execute("""
                INSERT INTO 运行数据 VALUES (?, ?, ?, ?)
                ON CONFLICT DO UPDATE SET
                    当前任务=excluded.当前任务,
                    上次更新时间=excluded.上次更新时间,
                    状态=excluded.状态
            """, (用户标识, 当前任务, time.time(), 状态))
            conn.commit()

    def 获取运行数据(self, 用户标识: str):
        """查询运行状态"""
        with self._获取连接() as conn:
            return conn.execute(
                "SELECT 当前任务, 上次更新时间, 状态 FROM 运行数据 WHERE 用户标识 = ?",
                (用户标识,)
            ).fetchone()


# ==== 用户任务线程 ====
class 用户任务线程:
    """集成化任务线程"""

    def __init__(self, 用户标识: str, 消息队列: queue.Queue, 数据库: 任务数据库):
        # 基础属性
        self.用户标识 = 用户标识
        self.消息队列 = 消息队列
        self.数据库 = 数据库
        self.状态 = "已停止"

        # 配置管理
        self.配置锁 = threading.RLock()
        self.用户设置 = self._加载设置()

        # 线程控制
        self.停止_flag = False
        self.线程锁 = threading.RLock()

    def _加载设置(self) -> 用户设置:
        """加载用户配置"""
        return self.数据库.获取用户设置(self.用户标识)

    def 更新设置(self, 新设置: 用户设置):
        """线程安全更新配置"""
        with self.配置锁:
            self.用户设置 = 新设置
            self.数据库.保存用户设置(self.用户标识, 新设置)

    def 开始工作(self):
        """启动任务线程"""
        if self.状态 != "已停止":
            return

        self.停止_flag = False
        self.主线程 = threading.Thread(
            target=self._任务流程,
            name=f"任务线程-{self.用户标识}",
            daemon=True
        )
        self.主线程.start()
        self.状态 = "运行中"
        self.数据库.更新运行数据(self.用户标识, "初始化", "运行中")

    def _任务流程(self):
        """主任务逻辑"""
        try:
            while not self.停止_flag:
                # 执行任务阶段
                self._执行阶段()

                # 记录心跳
                self._记录心跳()
        except Exception as e:
            self.状态 = "异常"
            self.数据库.更新运行数据(self.用户标识, "异常处理", "异常状态")
            self.消息队列.put(f"用户{self.用户标识} 异常: {str(e)}")

    def _执行阶段(self):
        """任务处理逻辑"""
        # 获取当前配置
        当前设置 = self.用户设置

        # 模拟任务处理
        self.数据库.更新运行数据(self.用户标识, "数据处理", "运行中")
        time.sleep(当前设置.任务参数.get("处理间隔", 1.0))

        self.数据库.更新运行数据(self.用户标识, "计算任务", "运行中")
        time.sleep(当前设置.任务参数.get("计算间隔", 2.0))

    def _记录心跳(self):
        """记录心跳日志"""
        当前设置 = self.用户设置
        下次超时 = time.time() + 当前设置.心跳间隔 * 3

        self.数据库.记录日志(
            self.用户标识,
            f"心跳检测 | 状态: {self.状态}",
            下次超时
        )
        # 修正方法名
        self.数据库.更新运行数据(self.用户标识, "心跳记录", "正常")

    def 检查超时(self) -> bool:
        """检查是否超时"""
        最后日志 = self.数据库.读取最后日志(self.用户标识)
        return time.time() > 最后日志.下次超时 if 最后日志 else False

    def 停止(self):
        """停止线程"""
        self.停止_flag = True
        if self.主线程.is_alive():
            self.主线程.join()
        self.状态 = "已停止"
        self.数据库.更新运行数据(self.用户标识, "停止", "已停止")


# ==== 监控中心 ====
class 任务监控中心:
    """增强型监控服务"""

    def __init__(self):
        self.活跃线程池 = {}
        self.消息队列 = queue.Queue()
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
        if 用户标识 in self.活跃线程池:
            raise ValueError("用户已存在")

        新线程 = 用户任务线程(用户标识, self.消息队列, self.数据库)
        if 初始设置:
            新线程.更新设置(初始设置)
        self.活跃线程池[用户标识] = 新线程
        新线程.开始工作()

    def _监控循环(self):
        """监控主循环"""
        while self.运行标志:
            # 检查任务状态
            for 用户标识, 线程 in list(self.活跃线程池.items()):
                if 线程.检查超时():
                    self.消息队列.put(f"用户{用户标识} 心跳超时，重启中...")
                    线程.停止()
                    线程.开始工作()

            # 处理消息
            self._处理消息()
            time.sleep(1)

    def _处理消息(self):
        """处理系统消息"""
        while not self.消息队列.empty():
            消息 = self.消息队列.get()
            print(f"[监控] {time.ctime()}: {消息}")
            self.消息队列.task_done()

    def 获取状态报告(self):
        """生成状态报告"""
        return {
            用户标识: {
                "设置": self.数据库.获取用户设置(用户标识).__dict__,
                "运行数据": self.数据库.获取运行数据(用户标识),
                "最后日志": self.数据库.读取最后日志(用户标识).日志内容 if self.数据库.读取最后日志(用户标识) else "无"
            }
            for 用户标识 in self.活跃线程池
        }


# ==== 使用示例 ====
if __name__ == "__main__":
    # 初始化系统
    监控中心 = 任务监控中心()

    # 创建自定义配置用户
    高级设置 = 用户设置(
        心跳间隔=3.0,
        任务参数={"处理间隔": 0.5, "计算间隔": 1.5}
    )
    监控中心.创建用户任务("VIP用户", 高级设置)

    # 创建默认配置用户
    监控中心.创建用户任务("普通用户")

    # 运行监控
    try:
        while True:
            报告 = 监控中心.获取状态报告()
            print("\n=== 系统状态 ===")
            for 用户, 数据 in 报告.items():
                print(f"{用户}:")
                print(f"  当前任务: {数据['运行数据'][0]}")
                print(f"  最后日志: {数据['最后日志'][:20]}")
                print(f"  心跳间隔: {数据['设置']['心跳间隔']}s")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n正在关闭系统...")
        监控中心.运行_flag = False
        for 用户 in 监控中心.活跃线程池.values():
            用户.停止()