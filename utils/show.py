import wx
import os
from utils.fpath import *
from utils.cus_button import button_icon
import utils.datafun as C
import utils.timefun as T
import utils.file_controls as FC
import time
import utils.Dlog as D


class ShowBlock(wx.Dialog):
    """显示项目记录界面"""
    def __init__(self):
        super().__init__(None, 2, "项目记录展示", size=(400, 280))
        self.app = wx.GetApp()
        self.panel = self.app.frame

        # 图标
        button_icon(self, "饭团.png")

        self.Center()

        buttonToday = wx.Button(self, label="Today")
        buttonToday.Bind(wx.EVT_BUTTON, self.today)

        buttonWeek = wx.Button(self, label="Week")
        buttonWeek.Bind(wx.EVT_BUTTON, self.week)

        buttonMonth = wx.Button(self, label="Month")
        buttonMonth.Bind(wx.EVT_BUTTON, self.month)

        buttonAll = wx.Button(self, label="All")
        buttonAll.Bind(wx.EVT_BUTTON, self.all)

        # 创建水平sizer
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # 在右侧添加一个弹簧以推动按钮
        hbox.AddStretchSpacer()

        # 添加按钮，并设置它们之间的间隔
        hbox.Add(buttonToday, flag=wx.RIGHT, border=10)
        hbox.Add(buttonWeek, flag=wx.RIGHT, border=10)
        hbox.Add(buttonMonth, flag=wx.RIGHT, border=10)
        hbox.Add(buttonAll, flag=wx.RIGHT, border=10)

        # 将水平sizer添加到垂直sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        vbox.Add(hbox, flag=wx.ALIGN_RIGHT | wx.ALL, border=20)

        info = "回首往昔，更进一步"
        st1 = wx.StaticText(self, label=info, style=wx.ALIGN_CENTER)
        vbox.Add((-1, 30))
        vbox.Add(st1, proportion=1, flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=20)
        vbox.Add((-1, 20))

        self.SetSizer(vbox)

    def today(self, e):
        info = C.readlog()
        dlg = D.RecDialog(None, 4, info, "当日记录")
        self.hish(dlg)

    def week(self, e):
        dlg = D.RecDialog_v1(1)
        self.hish(dlg)

    def month(self, e):
        dlg = D.RecDialog_v1(2)
        self.hish(dlg)

    def all(self, e):
        dlg = D.RecDialog_v1(3)
        self.hish(dlg)

    def hish(self, dlg):    # 窗口 隐藏->显示 代码重用
        # self.Hide()
        dlg.ShowModal()
        dlg.Destroy()
        # self.Show()