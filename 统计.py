import os


def 统计代码行数(目录):
    总行数 = 0
    注释行数 = 0
    空行数 = 0
    代码行数 = 0

    # 遍历目录及其子目录
    for 根, _, 文件名列表 in os.walk(目录):
        # 如果当前目录是 .venv 文件夹，跳过
        if '.venv' in 根:
            continue
        if 'rapidocr_onnxruntime' in 根:
            continue

        for 文件名 in 文件名列表:
            if 文件名.endswith(".py"):  # 只统计 Python 文件
                文件路径 = os.path.join(根, 文件名)
                with open(文件路径, 'r', encoding='utf-8') as f:
                    for 行号, 行 in enumerate(f, 1):
                        行 = 行.strip()
                        if not 行:  # 空行
                            空行数 += 1
                        elif 行.startswith("#"):  # 注释行1
                            注释行数 += 1
                        else:
                            代码行数 += 1
                        总行数 += 1

    print(f"总行数: {总行数}")
    print(f"代码行数: {代码行数}")
    print(f"注释行数: {注释行数}")
    print(f"空行数: {空行数}")


# 调用函数统计当前目录的代码量，排除 .venv 文件夹
统计代码行数(".")
