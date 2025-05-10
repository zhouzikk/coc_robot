# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from 模块.检测.OCR识别器.rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

img_url = r"模块/检测/rapidocr_onnxruntime/OCR_Test.png"
result = engine(img_url)
print(result)

result.vis("vis_result.jpg")
