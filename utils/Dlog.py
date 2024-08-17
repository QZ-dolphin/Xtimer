import wx
import os
from utils.fpath import *
from utils.cus_button import button_icon
import utils.datafun as C
import utils.timefun as T
import time

class TransparentText(wx.StaticText):
    """透明背景字幕"""
    def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TRANSPARENT_WINDOW | wx.ALIGN_LEFT | wx.EXPAND):
        wx.StaticText.__init__(self, parent, id, label=label, pos=pos, size=size, style=style)
        self.SetForegroundColour('white')
        self.text_lines = []
        self.UpdateText(label)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def UpdateText(self, text):
        self.text_lines = [text[i:i + 20] for i in range(0, len(text), 20)]
        for i in range(len(self.text_lines)):
            if self.text_lines[i][0] in {"，", "。", "！", "？", ",", ".", "!", "?"}:
                self.text_lines[i-1] += self.text_lines[i][0]
                self.text_lines[i] = self.text_lines[i][1:]
        self.Refresh()

    def on_paint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)
        font_face = self.GetFont()
        font_color = self.GetForegroundColour()
        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)

        y = 0
        for line in self.text_lines:
            dc.DrawText(line, 0, y+3)
            y += dc.GetCharHeight()

    def on_size(self, event):
        self.Refresh()
        event.Skip()


class StaDialog(wx.Dialog):
    def __init__(self, parent, id):
        super().__init__(parent, id, "开始（项目专用）", size=(350, 250))
        self.app = wx.GetApp()
        self.panel = self.app.frame

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label="所要进行的项目名称：")
        hbox1.Add(st1, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=20)
        self.proj = wx.TextCtrl(self)
        hbox1.Add(self.proj, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)

        vbox.Add((-1, 24))
        vbox.Add(hbox1, flag=wx.EXPAND)
        vbox.Add((-1, 24))
        info1, info2 = C.show_projs()
        st4 = wx.StaticText(self, label=info1)
        st5 = wx.StaticText(self, label=info2)
        st5.Wrap(280)
        vbox.Add(st4, flag=wx.LEFT, border=20)
        vbox.Add((-1, 4))
        vbox.Add(st5, flag=wx.LEFT, border=28)
        self.submit = wx.Button(self, label="开始计时")
        vbox.Add((-1, 30))
        vbox.Add(self.submit, flag=wx.ALIGN_CENTER)

        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.submit)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)
        # 图标
        button_icon(self, "process.png")
        self.Center()

    def OnClick(self, event):
        proj = self.proj.GetValue()
        if proj.strip() == "":
            dial = ShowInfoV1('请输入项目', '注意')
            dial.ShowModal()
            dial.Destroy()
            self.proj.Clear()
            return
        info = C.change_info(proj)
        dlg = TimDialog(None, 1, info, proj)
        self.Close()
        dlg.ShowModal()
        dlg.Destroy()

    def OnChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.OnClick(event)
        else:
            event.Skip()


class TimDialog(wx.Dialog):
    def __init__(self, parent, id, info, proj):
        super().__init__(parent, id, "计时开始", size=(350, 200))
        _, self.begin_t = T.da_hour()
        self.start_time = time.time()
        self.proj = proj
        self.app = wx.GetApp()
        self.panel = self.app.frame

        intro = wx.StaticText(self, label=info)
        self.submit_btn = wx.Button(self, label="结束计时")
        self.elapsed_time_label = wx.StaticText(self, label="", size=(300, -1), style=wx.ALIGN_CENTER)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_elapsed_time, self.timer)
        self.timer.Start(1000)  # 每1000毫秒（1秒）更新一次

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 24))
        vbox.Add(intro, flag=wx.LEFT, border=20)
        vbox.Add((-1, 24))

        vbox.Add(self.elapsed_time_label, proportion=1, flag=wx.ALIGN_CENTER)
        vbox.Add((-1, 24))
        vbox.Add(self.submit_btn, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=20)

        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.submit_btn)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnChar)

        # 图标
        button_icon(self, "日程安排.png")
        self.Center()
        # self.setPosition()

    def setPosition(self):
        # 获取屏幕尺寸
        screen_width, screen_height = wx.DisplaySize()
        # 获取对话框尺寸
        dialog_width, dialog_height = self.GetSize()

        # 计算对话框在屏幕右上角的位置
        x = screen_width - dialog_width
        y = 0
        # 设置对话框位置
        self.SetPosition((x, y))

    def update_elapsed_time(self, event):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        formatted_time = T.time_s2(elapsed_time)
        self.elapsed_time_label.SetLabel(f"计时中：{formatted_time}")

    def OnClick(self, event):
        self.timer.Stop()
        self.end_time = time.time()  # 记录结束时间
        C.setlog(self.proj, self.begin_t)   # 载入当日记录log中
        elapsed_time = self.end_time - self.start_time
        s = "您此次花费的的时间为: " + T.time_s2(elapsed_time)
        C.change_2(self.proj, elapsed_time) # 载入所有记录中
        dlg = ResDialog(None, 2, s)
        self.Close()
        dlg.ShowModal()
        dlg.Destroy()

    def OnChar(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            self.OnClick(event)
        else:
            event.Skip()


class ResDialog(wx.Dialog):
    """生成时间记录显示"""
    def __init__(self, parent, id, info):
        super(ResDialog, self).__init__(parent, id, "时间记录", size=(350, 200))
        self.app = wx.GetApp()
        self.panel = self.app.frame

        tx = wx.StaticText(self, label=info, size=(300, 20), style=wx.ALIGN_CENTER)
        button_ok = wx.Button(self, wx.ID_OK)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 50))
        vbox.Add(tx, proportion=1, flag=wx.ALIGN_CENTER)
        vbox.Add(button_ok, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=20)
        self.SetSizer(vbox)

        # 图标
        button_icon(self, "生成报告.png")
        self.Center()


class ShowInfoV1(wx.Dialog):
    """显示普通的提示信息，短文本"""
    def __init__(self, info, title):
        super().__init__(None, 12, title, size=(300, 200))
        self.app = wx.GetApp()
        self.panel = self.app.frame
        self.Center()
        button_icon(self, "show.png")

        vbox = wx.BoxSizer(wx.VERTICAL)
        # tc1 = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL)
        # tc1.SetValue(info)

        st1 = wx.StaticText(self, label=info, style=wx.ALIGN_CENTER)
        vbox.Add((-1, 50))
        vbox.Add(st1, proportion=1, flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=20)
        vbox.Add((-1, 20))
        buttonok = wx.Button(self, wx.ID_OK)
        vbox.Add(buttonok, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=15)

        self.SetSizer(vbox)


class ShowInfoV2(wx.Dialog):
    """显示普通的提示信息，长文本"""
    def __init__(self, info, title):
        super().__init__(None, 13, title, size=(300, 200))
        self.app = wx.GetApp()
        self.panel = self.app.frame
        self.Center()
        button_icon(self, "show.png")

        vbox = wx.BoxSizer(wx.VERTICAL)
        tc1 = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL)
        tc1.SetValue(info)
        vbox.Add((-1, 10))
        vbox.Add(tc1, proportion=1, flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=20)
        vbox.Add((-1, 20))
        buttonok = wx.Button(self, wx.ID_OK)
        vbox.Add(buttonok, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=15)

        self.SetSizer(vbox)