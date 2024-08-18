import matplotlib.pyplot as plt
from utils.fpath import *


def draw_bar_chart(xlabel, yvalue):
    plt.figure(num=1, figsize=(7, 5), )
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['axes.unicode_minus'] = False

    # 设置颜色列表，前两个柱状图为红色，其余为默认颜色
    colors = []
    for i in range(len(xlabel)):
        if i<2:
            colors.append('orangered')
        elif i<5:
            colors.append('tomato')
        elif i<8:
            colors.append('coral')
        else:
            colors.append('wheat')

    plt.bar(xlabel, yvalue, color=colors)
    plt.ylabel('时间/h', fontsize=14)  # 设置 y 轴标签
    plt.grid(True, linestyle='--')
    plt.tick_params(axis='both', which='major', labelsize=14)
    if os.path.exists(RP_Path):
        os.remove(RP_Path)
    plt.savefig(RP_Path, format='png', bbox_inches='tight')
    plt.close()