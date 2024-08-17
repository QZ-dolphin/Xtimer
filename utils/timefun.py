import time
from datetime import datetime
import os
from utils.fpath import *


def da_hour():
    """返回天和小时"""
    t = time.localtime(time.time())
    data = time.strftime('%Y-%m-%d', t)
    hour = time.strftime('%H:%M', t)
    return data, hour


def format_time(seconds):
    """时间格式化返回"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), int(seconds)


def time_s2(elapsed_time):
    """返回花费时间字符串"""
    formatted_time = format_time(elapsed_time)
    s = f"{formatted_time[0]} 小时, {formatted_time[1]} 分钟, {formatted_time[2]} 秒"
    return s


def month_filepath():
    """返回月度记录文件路径"""
    t = time.localtime(time.time())
    date = time.strftime('%Y%m', t)
    filename = "M" + date + ".json"
    return os.path.join(Log_Path, filename)


def week_filepath():
    """返回当周记录文件路径"""
    today = datetime.today()
    week_number = today.isocalendar()[1]
    filename = f"W{today.year}{week_number}.json"
    return os.path.join(Log_Path, filename)
