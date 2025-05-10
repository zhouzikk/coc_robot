# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from 模块.检测.rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

img_url = r"C:\Users\Hello\Desktop\coc\RapidOCR\python\rapidocr_onnxruntime\img.png"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
