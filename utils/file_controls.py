import os
import random
import json
from utils.fpath import *


def checkfile(filename):
    """检查文件是否存在，不存在则创建文件"""
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(filename):
        # 创建文件
        with open(filename, 'w') as file:
            pass


def jsonload(filepath, value):
    """检查json读取情况"""
    checkfile(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = value
    return data


def re_projs_t(filepath):
    """返回项目及时间字典"""
    checkfile(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}
    return data


def re_projs(filepath):
    """返回项目列表"""
    data = re_projs_t(filepath)
    return list(data.keys())


def lyrics():
    """设置主界面名言名句"""
    info = []
    # 打开文件并逐行读取内容
    with open(Lyr_Path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除每行末尾的换行符，并添加到列表中
            info.append(line.strip())
    random.shuffle(info)
    return info
