

import os
import sys
import subprocess

import os
import sys
import subprocess

def 获取版本号():
    # 判断是否是打包运行（如 PyInstaller 的 _MEIPASS）
    是否打包环境 = hasattr(sys, '_MEIPASS')

    # 路径设定
    当前目录 = sys._MEIPASS if 是否打包环境 else os.path.dirname(os.path.abspath(__file__))
    版本路径 = os.path.join(当前目录, "版本号.txt")

    # 打包环境：直接读取版本文件
    if 是否打包环境 and os.path.exists(版本路径):
        with open(版本路径, "r", encoding="utf-8") as f:
            return f.read().strip()

    # 非打包环境：尝试获取当前 tag（如果 HEAD 正好在 tag 上）
    try:
        简洁版本号 = subprocess.check_output(
            ["git", "describe", "--tags", "--exact-match"],
            stderr=subprocess.DEVNULL, encoding="utf-8"
        ).strip()
        return 简洁版本号
    except subprocess.CalledProcessError:
        pass  # HEAD 不在 tag 上，继续 fallback

    # fallback：获取最近 tag，不含提交数
    try:
        复杂版本号 = subprocess.check_output(
            ["git", "describe", "--tags"],
            stderr=subprocess.DEVNULL, encoding="utf-8"
        ).strip()
        return 复杂版本号.split("-")[0]  # 截取最近 tag 名
    except Exception:
        pass

    # 最后 fallback：读取本地版本号文件
    if os.path.exists(版本路径):
        with open(版本路径, "r", encoding="utf-8") as f:
            return f.read().strip()

    return "unknown"


