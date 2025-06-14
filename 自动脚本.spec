# 自动脚本.spec
# -*- mode: python ; coding: utf-8 -*-
import os
import subprocess

from PyInstaller.utils.hooks import collect_submodules

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# 项目根目录（根据你的实际情况调整）
项目根 = os.path.abspath(os.getcwd())
# 版本号文件路径（相对于项目根目录）
版本号文件 = os.path.join(项目根, "工具包", "版本号.txt")
# 生成版本号文件（打包前执行）
print("正在生成版本号文件...")

env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"
subprocess.run(
    ["python", os.path.join(项目根, "工具包", "生成版本号文件.py")],
    check=True,
    env=env
)



block_cipher = None

a = Analysis(
    ['UI入口.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('img/*.*', 'img'),
        ('模块/**/*.*', '模块'),
        ('数据库/*.*', '数据库'),
        ('核心/op-0.4.5_with_model/tools.dll', 'op-0.4.5_with_model/'),
        ('核心/op-0.4.5_with_model/op_x64.dll', 'op-0.4.5_with_model/'),
        ('模块/检测/OCR识别器/rapidocr_onnxruntime/config.yaml','模块/检测/OCR识别器/rapidocr_onnxruntime/'),
        ('模块/检测/OCR识别器/rapidocr_onnxruntime/models/*.*','模块/检测/OCR识别器/rapidocr_onnxruntime/models/'),
        ('模块/检测/YOLO检测器/模型/*.*','模块/检测/YOLO检测器/模型/'),
        ('版本号.txt', ".")
    ],
    hiddenimports=collect_submodules('模块') + collect_submodules('核心'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='游戏辅助',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True  # 如不想显示黑框请改为 False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='游戏辅助'
)
