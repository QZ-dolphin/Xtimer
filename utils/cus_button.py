import wx


class DesButton(wx.BitmapButton):
    def __init__(self, place, image1, image2, size, pos):
        self.image1 = self.scale_bitmap(image1, size)
        self.image2 = self.scale_bitmap(image2, size)
        super().__init__(place, wx.ID_ANY, self.image1, size=size, pos=pos, style=wx.BORDER_SIMPLE)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseOver)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

    def scale_bitmap(self, bitmap, size):
        image = bitmap.ConvertToImage()
        image = image.Scale(size[0], size[1], wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)

    def OnMouseOver(self, event):
        # 鼠标悬浮时切换到高亮图片
        self.SetBitmap(self.image2)

    def OnMouseLeave(self, event):
        # 鼠标离开时切换回普通图片
        self.SetBitmap(self.image1)
