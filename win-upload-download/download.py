# -*- coding: utf-8 -*-
__author__ = 'xiuery.com'

import time
import win32con
import win32gui


class Download:
    wnd_class = ''
    wnd_caption = ''

    def __init__(self, wnd_class='#32770', wnd_caption='另存为'):
        self.wnd_class = wnd_class
        self.wnd_caption = wnd_caption

    def start(self, filename):
        """
        获取下载窗口并完成下载
        """
        # 获取下载窗口
        window = win32gui.FindWindow(self.wnd_class, self.wnd_caption)

        # 寻找输入框Edit对象的句柄
        dui_view_wnd_class_name = win32gui.FindWindowEx(window, 0, 'DUIViewWndClassName', None)
        direct_ui_h_wnd = win32gui.FindWindowEx(dui_view_wnd_class_name, 0, 'DirectUIHWND', None)
        float_not_fy_sink = win32gui.FindWindowEx(direct_ui_h_wnd, 0, 'FloatNotifySink', None)
        com_box = win32gui.FindWindowEx(float_not_fy_sink, 0, 'ComboBox', None)
        edit = win32gui.FindWindowEx(com_box, 0, 'Edit', None)

        # 往输入框输入文件的绝对路径
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filename)

        # 确定按钮Button
        time.sleep(0.1)
        button = win32gui.FindWindowEx(window, 0, 'Button', None)
        win32gui.SendMessage(window, win32con.WM_COMMAND, 1, button)


if __name__ == '__main__':
    time.sleep(10)

    # download
    download = Download()
    download.start('C:\\abc.mht')
