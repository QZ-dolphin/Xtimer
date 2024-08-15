import os
import random
import json
from utils.fpath import *


def checkfile(filename):
    """检查文件是否存在，不存在则创建文件"""
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