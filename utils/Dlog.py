import wx


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