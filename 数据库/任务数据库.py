# ==== 数据库管理 ====
import json
import sqlite3
import time
from dataclasses import dataclass
from typing import List

@dataclass
class 任务日志:
    用户标识: str
    日志内容: str
    记录时间: float
    下次超时: float

@dataclass
class 用户设置:
    雷电模拟器索引:int=1
    服务器:str="国际服"
    部落冲突包名:str=("com.supercell.clashofclans" if 服务器 == "国际服" else "com.tencent.tmgp.supercell.clashofclans")



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

            # 用户设置表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS 用户设置 (
                    用户标识 TEXT PRIMARY KEY,
                    设置JSON TEXT
                )""")


    # ==== 日志操作 ====
    def 记录日志(self, 用户标识: str, 日志内容: str, 下次超时: float):
        """原子化日志记录
        下次超时:为下次超时的时间戳
        """
        with self._获取连接() as conn:
            游标 = conn.execute(
                "INSERT INTO 任务日志 (用户标识, 日志内容, 记录时间, 下次超时) VALUES (?, ?, ?, ?)",
                (用户标识, 日志内容, time.time(), 下次超时)
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

if __name__ == "__main__":
    数据库 = 任务数据库()

    # 保存一个用户设置
    设置 = 用户设置(雷电模拟器索引=2, 服务器="国内服")
    数据库.保存用户设置("用户001", 设置)

    # 读取该用户设置
    获取设置 = 数据库.获取用户设置("用户001")
    print("获取的设置：", 获取设置)

    # 添加一条日志
    数据库.记录日志("用户0021", "任务启动成功", time.time() + 60)

    # 获取最后日志
    最后日志 = 数据库.读取最后日志("用户001")
    print("最后一条日志：", 最后日志)

    # 查询历史日志
    日志列表 = 数据库.查询日志历史("用户001", 最大条数=5)
    for 日志 in 日志列表:
        print("历史日志：", 日志)
    print(数据库.获取用户设置("用户0021"))
