import wx
import time
from PIL import Image

from utils import version as V
from utils import Dlog as D
from utils import file_controls as FC
from utils import cus_button as CB
import utils.datafun as C
from utils.fpath import *
from utils.IDS import *
from utils.show import ShowBlock


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(550, 340))
        self.initUI()
        self.lockSize()

    def initUI(self):
        self.panel = wx.Panel(self, -1)
        self.ix = 42    # 按键定位
        self.iy = 63

        # 设置窗口背景图
        bisize = (550, 340)
        bgimage = self.image_fun("./res/pics/bgimage2.png", bisize)
        self.bgimage = wx.StaticBitmap(self.panel, -1, bgimage, pos=(0, -20))

        self.setLyr()  # 设置文案显示
        self.setBar()  # 设置状态栏
        self.setupIcon()  # 设置软件Icon
        self.setButton()  # 设置软件按键
        self.setMenu()  # 设置菜单

        self.Center()

    def lockSize(self):
        """锁定窗口大小"""
        self.SetMinSize((550, 340))
        self.SetMaxSize((550, 340))

    def image_fun(self, path, size):
        """设置窗口背景图"""
        img = Image.open(path)
        imsize = size
        img = img.resize(imsize, Image.LANCZOS)  # 指定目标尺寸并使用抗锯齿算法
        img = img.convert("RGB")  # 将图像转换为RGB模式，wx.Bitmap需要RGB图像
        # 创建 wx.StaticBitmap 控件，并将缩放后的图像转换为 wx.Bitmap
        width, height = img.size
        image = wx.Image(width, height)
        image.SetData(img.convert("RGB").tobytes())
        bmp = wx.Bitmap(image)
        return bmp

    def setLyr(self):
        """设置文案显示"""
        self.lyrs = FC.lyrics()
        self.lyr_index = 0
        self.timer2 = wx.PyTimer(self.LyrChange)
        self.timer2.Start(12000, wx.TIMER_CONTINUOUS)
        self.lyr = D.TransparentText(self.bgimage, label=self.lyrs[self.lyr_index], pos=(self.ix + 190, 140),
                                     size=(245, 300))

    def LyrChange(self):
        """文案显示切换"""
        self.lyr.Destroy()
        self.lyr_index += 1
        self.lyr_index %= len(self.lyrs)
        self.lyr = D.TransparentText(self.bgimage, label=self.lyrs[self.lyr_index], pos=(self.ix + 190, 140),
                                     size=(245, 300))

    def setBar(self):
        """创建状态栏"""
        sb = self.CreateStatusBar(2)
        self.SetStatusWidths([-1, -2])
        self.SetStatusText("Created by DQZ", 0)

        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.Notify()

    def Notify(self):
        """状态栏时间修改"""
        t = time.localtime(time.time())
        st = time.strftime('%Y-%m-%d  %H:%M:%S', t)
        self.SetStatusText(st, 1)

    def setupIcon(self):
        """设置软件Icon"""
        self.icon_path = os.path.join(Pic_Path, "logo.png")
        icon = wx.Icon(self.icon_path, type=wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

    ########################################################################################################
    ## 以下设置软件主界面按键

    def setButton(self):
        """设置软件按键"""
        size = (60, 30)

        image1 = wx.Bitmap("./res/pics/buttons/start.png", wx.BITMAP_TYPE_PNG)
        image2 = wx.Bitmap("./res/pics/buttons/start_highlight.png", wx.BITMAP_TYPE_PNG)
        self.button_start = CB.DesButton(self.bgimage, image1, image2, size, (self.ix, self.iy))
        self.panel.Bind(wx.EVT_BUTTON, self.OnClick, self.button_start)

        image3 = wx.Bitmap("./res/pics/buttons/show2.png", wx.BITMAP_TYPE_PNG)
        image4 = wx.Bitmap("./res/pics/buttons/show_highlight.png", wx.BITMAP_TYPE_PNG)
        self.button_show = CB.DesButton(self.bgimage, image3, image4, size, (self.ix, self.iy+60))
        self.panel.Bind(wx.EVT_BUTTON, self.OnClick, self.button_show)

        image5 = wx.Bitmap("./res/pics/buttons/del.png", wx.BITMAP_TYPE_PNG)
        image6 = wx.Bitmap("./res/pics/buttons/del_highlight.png", wx.BITMAP_TYPE_PNG)
        self.button_del = CB.DesButton(self.bgimage, image5, image6, size, (self.ix, self.iy+120))
        self.panel.Bind(wx.EVT_BUTTON, self.OnClick, self.button_del)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnClick(self, event):
        if event.GetEventObject() == self.button_start:
            self.start_()
        elif event.GetEventObject() == self.button_del:
            self.del_()
        elif event.GetEventObject() == self.button_show:
            self.show_()

    def hish(self, dlg):    # 窗口 隐藏->显示 代码重用
        self.Hide()
        dlg.ShowModal()
        dlg.Destroy()
        self.Show()

    def start_(self):
        dlg = D.StaDialog(None, -1)
        self.hish(dlg)

    def del_(self):
        dlg = D.DelDialog()
        self.hish(dlg)

    def show_(self):
        dlg = ShowBlock()
        self.hish(dlg)
    ######### 以上主界面功能按键代码
    ##########################################################################################################
    def OnCloseWindow(self, e):  # 窗口关闭确认
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
                                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            self.Destroy()
        else:
            e.Veto()    # 用于取消（否决）当前事件的处理,取消关闭事件

    def setMenu(self):
        """设置菜单"""
        menubar = wx.MenuBar()

        fmenu = wx.Menu()  # 创建子菜单项 "File"
        ab_menu = wx.MenuItem(fmenu, ID_ABOUT, "使用说明(&H)", "How to use this tool")
        ab_menu.SetBitmap(wx.Bitmap(os.path.join(Icon_Path, "ab.png")))
        up_menu = wx.MenuItem(fmenu, ID_UPDATE, "更新日志(&U)", "Details of Update")
        up_menu.SetBitmap(wx.Bitmap(os.path.join(Icon_Path, "up.png")))
        fmenu.Append(ab_menu)
        fmenu.Append(up_menu)

        menubar.Append(fmenu, "关于")  # 将 "MI" 添加到菜单栏

        tmenu = wx.Menu()  # 创建子菜单项 "File"
        ct_menu = wx.MenuItem(fmenu, ID_CAT, "类别标签(&C)", "Categories setting")
        ct_menu.SetBitmap(wx.Bitmap(os.path.join(Icon_Path, "ab.png")))
        tmenu.Append(ct_menu)

        ad_menu = wx.MenuItem(fmenu, ID_ADD, "项目导入(&A)", "Add project and its time")
        ad_menu.SetBitmap(wx.Bitmap(os.path.join(Icon_Path, "Targets.png")))
        tmenu.Append(ad_menu)
        # 查看记录功能
        lk_menu = wx.MenuItem(fmenu, ID_LOOK, "查看当日记录(&L)", "Today's records")
        lk_menu.SetBitmap(wx.Bitmap(os.path.join(Icon_Path, "饭团.png")))
        tmenu.Append(lk_menu)
        # 琐事记录功能
        dy_menu = wx.MenuItem(fmenu, ID_DAY, "日常琐事(&D)", "Daily routine")
        dy_menu.SetBitmap(wx.Bitmap(os.path.join(Icon_Path, "米饭.png")))
        tmenu.Append(dy_menu)

        menubar.Append(tmenu, "更多功能")

        self.SetMenuBar(menubar)


class App(wx.App):
    def __init__(self):
        super().__init__()

    def OnInit(self):
        self.flag = FLAG
        self.version = V.version_control(Version_Path, self.flag)
        self.title = "XTimer v." + self.version
        self.frame = MainFrame(None, -1, self.title)
        self.frame.Show(True)

        return True


FLAG = True
app = App()
app.MainLoop()
