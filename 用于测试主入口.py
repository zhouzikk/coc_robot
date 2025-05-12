# ==== 数据库改进设计 ====
import json
import os
import sqlite3
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class 运行时状态:
    机器人标志: str
    记录时间: float
    状态数据: Dict[str, Any]  # 使用字典存储动态状态


@dataclass
class 任务日志:
    机器人标志: str
    日志内容: str
    记录时间: float
    下次超时: float


@dataclass
class 机器人设置:
    雷电模拟器索引: int = 1
    服务器: str = "国际服"
    部落冲突包名: str = None

    def __post_init__(self):
        self.部落冲突包名 = ("com.supercell.clashofclans"
                             if self.服务器 == "国际服" else
                             "com.tencent.tmgp.supercell.clashofclans")


class 任务数据库:
    """增强型数据库管理"""

    def __init__(self, 文件路径=os.path.join(os.path.dirname(__file__), '任务系统.db')):
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
        """使用新版表结构"""
        with self._获取连接() as conn:
            # 状态记录表（支持任意状态类型）
            conn.execute("""
                CREATE TABLE IF NOT EXISTS 运行时状态 (
                    记录ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    机器人标志 TEXT NOT NULL,
                    记录时间 REAL NOT NULL,
                    状态类型 TEXT NOT NULL,  -- 如：resources/builder/upgrade_queue
                    状态值 TEXT NOT NULL    -- JSON格式存储
                )""")

            # 保留原有日志表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS 任务日志 (
                    记录ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    机器人标志 TEXT NOT NULL,
                    日志内容 TEXT,
                    记录时间 REAL NOT NULL,
                    下次超时 REAL NOT NULL
                )""")

            # 保留原有设置表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS 机器人设置 (
                    机器人标志 TEXT PRIMARY KEY,
                    设置JSON TEXT
                )""")

    # ==== 新版状态操作方法 ====
    def 更新状态(self, 机器人标志: str, 状态类型: str, 状态数据: Any):
        """原子化状态更新（保留历史记录）"""
        with self._获取连接() as conn:
            conn.execute(
                """INSERT INTO 运行时状态 
                (机器人标志, 记录时间, 状态类型, 状态值)
                VALUES (?, ?, ?, ?)""",
                (机器人标志, time.time(), 状态类型, json.dumps(状态数据))
            )
            conn.commit()

    def 获取最新完整状态(self, 机器人标志: str) -> 运行时状态:
        """合并所有类型的最新状态"""
        完整状态 = {}
        类型列表 = ['resources', 'builder', 'upgrade_queue', 'war_status']  # 可扩展

        with self._获取连接() as conn:
            for 类型 in 类型列表:
                结果 = conn.execute("""
                    SELECT 状态值 
                    FROM 运行时状态 
                    WHERE 机器人标志 = ? AND 状态类型 = ?
                    ORDER BY 记录ID DESC 
                    LIMIT 1
                """, (机器人标志, 类型)).fetchone()

                if 结果:
                    完整状态[类型] = json.loads(结果[0])

        return 运行时状态(
            机器人标志=机器人标志,
            记录时间=time.time(),
            状态数据=完整状态
        )

    def 获取状态历史(self, 机器人标志: str,
                     状态类型: Optional[str] = None,
                     起始时间: float = 0,
                     截止时间: float = None,
                     最大条数: int = 500) -> List[Dict]:
        """通用历史查询"""
        截止时间 = 截止时间 or time.time()
        查询参数 = [机器人标志, 起始时间, 截止时间, 最大条数]
        类型条件 = ""

        if 状态类型:
            类型条件 = "AND 状态类型 = ?"
            查询参数.insert(3, 状态类型)

        with self._获取连接() as conn:
            records = conn.execute(f"""
                SELECT 记录时间, 状态类型, 状态值 
                FROM 运行时状态
                WHERE 机器人标志 = ? 
                  AND 记录时间 BETWEEN ? AND ?
                  {类型条件}
                ORDER BY 记录时间 DESC
                LIMIT ?
            """, 查询参数).fetchall()

        return [{
            "时间": row[0],
            "类型": row[1],
            "数据": json.loads(row[2])
        } for row in records]


# 使用示例
if __name__ == "__main__":
    数据库 = 任务数据库()

    # 分次更新不同状态
    数据库.更新状态("机器人001", "resources", {
        "gold": 1500000,
        "elixir": 800000,
        "dark_elixir": 2000
    })

    数据库.更新状态("机器人001", "builder", {
        "free_builders": 2,
        "total_builders": 5
    })

    数据库.更新状态("机器人001", "upgrade_queue", {
        "current_upgrade": "箭塔",
        "remaining_time": 3600  # 秒
    })

    # 获取完整状态
    当前状态 = 数据库.获取最新完整状态("机器人001")
    print("当前完整状态：")
    print(f"- 资源：{当前状态.状态数据.get('resources')}")
    print(f"- 工人：{当前状态.状态数据.get('builder')}")
    print(f"- 升级队列：{当前状态.状态数据.get('upgrade_queue')}")

    # 查询资源历史
    print("\n资源变化历史：")
    for 记录 in 数据库.获取状态历史("机器人001", "resources", 最大条数=3):
        print(f"[{time.ctime(记录['时间'])}] {记录['数据']}")