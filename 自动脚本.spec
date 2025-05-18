# 自动脚本.spec
# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['测试入口2.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('img/*.*', 'img'),
        ('模块/**/*.*', '模块'),
        ('数据库/*.*', '数据库'),
        ('核心/op-0.4.5_with_model/', 'op-0.4.5_with_model'),
        ('模块/检测/OCR识别器/rapidocr_onnxruntime/config.yaml','模块/检测/OCR识别器/rapidocr_onnxruntime/'),
        ('模块/检测/OCR识别器/rapidocr_onnxruntime/models/*.*','模块/检测/OCR识别器/rapidocr_onnxruntime/models/'),
        ('模块/检测/YOLO检测器/模型/*.*','模块/检测/YOLO检测器/模型/')
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
