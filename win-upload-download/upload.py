# -*- coding: utf-8 -*-
__author__ = 'xiuery.com'

import time
import win32con
import win32gui


class Upload:
    wnd_class = ''
    wnd_caption = ''

    def __init__(self, wnd_class='#32770', wnd_caption='打开'):
        self.wnd_class = wnd_class
        self.wnd_caption = wnd_caption

    def start(self, filename):
        """
        获取上传窗口并完成上传
        """
        # 获取上传窗口
        window = win32gui.FindWindow(self.wnd_class, self.wnd_caption)

        # 寻找输入框Edit对象的句柄
        combo_box_ex32 = win32gui.FindWindowEx(window, 0, 'ComboBoxEx32', None)
        combo_box = win32gui.FindWindowEx(combo_box_ex32, 0, 'ComboBox', None)
        edit = win32gui.FindWindowEx(combo_box, 0, 'Edit', None)

        # 往输入框输入文件的绝对路径
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filename)

        # 确定按钮Button
        time.sleep(0.1)
        button = win32gui.FindWindowEx(window, 0, 'Button', None)
        win32gui.SendMessage(window, win32con.WM_COMMAND, 1, button)


if __name__ == '__main__':
    time.sleep(10)

    # upload
    upload = Upload()
    upload.start('C:\\abc.mht')
