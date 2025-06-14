import os
import subprocess

from PyInstaller.utils.hooks import collect_submodules

# 项目根目录（根据你的实际情况调整）
项目根 = os.path.abspath(os.path.dirname(__file__))

# 版本号文件路径（相对于项目根目录）
版本号文件 = os.path.join(项目根, "工具包", "版本号.txt")

# 生成版本号文件（打包前执行）
print("正在生成版本号文件...")
subprocess.run(["python", os.path.join(项目根, "工具包", "生成版本号文件.py")], check=True)
