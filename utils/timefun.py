import time


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