import json
import time
import utils.file_controls as FC
import utils.timefun as T
from utils.fpath import *


def change_info(proj):
    """生成项目已花费时间"""
    projs = {}
    projs = FC.jsonload(File_Path, projs)
    if proj in projs.keys():
        t = T.time_s2(float(projs[proj]))
        info1 = f"{proj} 已花费时间: {t}"
    else:
        info1 = f"欢迎开始新项目 {proj}"
    return info1


def show_projs():
    """返回已有项目"""
    projs = {}
    projs = FC.jsonload(File_Path, projs)
    info1 = "已有项目："
    info2 = ""
    for proj in projs.keys():
        info2 = info2 + proj + " "
    return info1, info2


def setlog(proj, begin_t):
    """设置每日记录"""
    data, end_t = T.da_hour()

    log_path = os.path.join(Log_Path, f"{data}.txt")
    info = f"{begin_t} - {end_t}\t{str(proj)}\n"

    if not os.path.exists(log_path):
        with open(log_path, 'w', encoding='utf-8') as file:
            file.write(f"{data}\n")

    with open(log_path, 'a', encoding='utf-8') as file:
        file.write(info)


def change_3(proj, edt):
    """添加至总记录中"""
    projs = {}
    projs = FC.jsonload(File_Path, projs)
    if proj not in projs.keys():
        projs[proj] = 0.0
    t = projs[proj] + edt
    projs[proj] = t

    with open(File_Path, "w", encoding='utf-8') as f:
        json.dump(projs, f)


def change_2(proj, edt):
    """添加至所有记录中"""
    monthFilePath = T.month_filepath()
    weekFilePath = T.week_filepath()
    change_1(monthFilePath, proj, edt)
    change_1(weekFilePath, proj, edt)
    change_1(File_Path, proj, edt)


def change_1(filepath, proj, edt):
    """添加记录"""
    projs = {}
    projs = FC.jsonload(filepath, projs)
    if proj not in projs.keys():
        projs[proj] = 0.0
    t = projs[proj] + edt
    projs[proj] = t

    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(projs, f)