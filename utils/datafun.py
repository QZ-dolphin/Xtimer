import json
import time
import utils.file_controls as FC
import utils.timefun as T
from utils.fpath import *
import utils.draw as DW


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


def show_info(filepath):
    """返回项目及时间"""
    projs_t = {}
    projs_t = FC.jsonload(filepath, projs_t)

    s = "项目名称"
    info = f"{s.ljust(10)}\t已花费时间\n"

    Xlabel = []
    Yvalue = []
    k = 0

    for projs, pro_t in projs_t.items():
        t = T.time_s2(float(pro_t))
        info += f"· {projs.ljust(10)}\t{t}\n"
        t = float(pro_t) / 3600
        t1 = round(t, 1)
        k += 1
        if t1 >= 0.1 and k <= 10:
            Xlabel.append(projs)
            Yvalue.append(t1)
    # print(Xlabel)
    combined = list(zip(Xlabel, Yvalue))
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)

    # 解压排序后的结果回两个列表
    Xlabel, Yvalue = zip(*sorted_combined)

    # 将元组转换回列表
    Xlabel = list(Xlabel)
    Yvalue = list(Yvalue)
    DW.draw_bar_chart(Xlabel, Yvalue)
    return info


def setlog(proj, begin_t):
    """设置每日记录"""
    data, end_t = T.da_hour()
    if not os.path.exists(Log_Path):
        os.makedirs(Log_Path)
    log_path = os.path.join(Log_Path, f"{data}.txt")
    info = f"{begin_t} - {end_t}\t{str(proj)}\n"

    if not os.path.exists(log_path):
        with open(log_path, 'w', encoding='utf-8') as file:
            file.write(f"{data}\n")

    with open(log_path, 'a', encoding='utf-8') as file:
        file.write(info)


##############################################################################
### 以下删除记录代码

def del_2(filepath, proj):
    projs_t = {}
    projs_t = FC.jsonload(filepath, projs_t)
    if proj in projs_t.keys():
        del projs_t[proj]
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(projs_t, f)












##############################################################################
## 以下改变记录代码
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

#######  以上改变记录代码
####################################################################################
