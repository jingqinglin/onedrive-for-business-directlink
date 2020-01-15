# coding:utf-8
import tkinter
from tkinter import ttk
from tkinter import messagebox

import pyperclip
import requests
import threading

import os
import sys
import win32con
import win32gui
import win32print
import ctypes
import math

import entryplaceholder
import directlink


# 重定向线程
class UrlRedirecctThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        req = requests.get(entry_url.get())
        redirectUrl = req.url
        print(req.status_code)
        imgResult = imgPattern in redirectUrl
        print('redirect url: ' + redirectUrl + '\n')
        print(imgResult)
        label_tip.config(text='')
        if imgResult:
            # 创建对象，调用类方法
            transferObj = directlink.TransferToDirectlink(redirectUrl)
            directUrl = transferObj.imgHosting()
            label_directlink.config(text=directUrl)
            pyperclip.copy(directUrl)
            pyperclip.paste()
        elif result or '_layouts/52/download.aspx?share=' in redirectUrl:
            messagebox.showwarning(title='警告', message='此链接可能不是图片类型的文件，请点击“下载直链”')



# 修正 ico 图标路径
# https://blog.csdn.net/you227/article/details/46989625
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        print(os.path.join(sys._MEIPASS,relative))
        return os.path.join(sys._MEIPASS,relative)
    print('relative: ' + os.path.join(relative))
    return os.path.join(relative)

win = tkinter.Tk()
icoPath = resource_path(r'./OneDrive.ico')
if os.path.exists(icoPath):
    win.iconbitmap(icoPath)
win.title('OneDrive for Business 直链')


# https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp
# win.winfo_screenheight() & win.winfo_screenwidth() 会根据Windows缩放比例变化，无法计算正确的 dpi
# 参考 https://www.cnblogs.com/micenote/p/12165669.html 获取屏幕分辨率
hDC = win32gui.GetDC(0)
# 横向分辨率
HORZRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
# 纵向分辨率
VERTRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
def get_dpi():
    MM_TO_IN = 1/25.4
    pxw = math.sqrt(pow(HORZRES, 2) + pow(VERTRES, 2))
    inw = math.sqrt(pow(win.winfo_screenmmwidth(), 2) + pow(win.winfo_screenmmheight(), 2)) * MM_TO_IN
    return pxw/inw
# PROCESS_DPI_UNAWARE            = 0,
# PROCESS_SYSTEM_DPI_AWARE       = 1,
# PROCESS_PER_MONITOR_DPI_AWARE  = 2
ctypes.windll.shcore.SetProcessDpiAwareness(1)
win.tk.call('tk', 'scaling', get_dpi()/72)
win.geometry(("%dx%d+%d+%d" % (HORZRES/2, VERTRES/2, HORZRES/4, VERTRES/4)))


frame_oriStr = ttk.LabelFrame(win, text="原链接", labelanchor="nw")
# rel 代表 relative
frame_oriStr.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.2)

# 获取剪贴板，设置 Entry 组件
clipboard = pyperclip.paste()
pattern = '-my.sharepoint.com/'
imgPattern = 'onedrive.aspx?'
result = pattern in clipboard
imgResult = imgPattern in clipboard
if (result or imgResult):
    entry_url = entryplaceholder.EntryWithPlaceholder(frame_oriStr, placeholder=clipboard, color='black')
else:
    entry_url = entryplaceholder.EntryWithPlaceholder(frame_oriStr, placeholder='请输入或粘贴正确的链接')

entry_url.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.90)

# 设置 Label 组件
frame_directlink = ttk.LabelFrame(win, text="直链", labelanchor="nw")
frame_directlink.place(relx=0.01, rely=0.3, relwidth=0.98, relheight=0.3)
label_directlink = tkinter.Label(frame_directlink, justify='left', wraplength=win.winfo_screenwidth() * 0.95)
label_directlink.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.90)

label_tip = tkinter.Label(win, justify='left')
label_tip.place(relx=0.01, rely=0.6, relwidth=0.15, relheight=0.1)


def fileDownloading():
    result = pattern in entry_url.get()
    transferObj = directlink.TransferToDirectlink(entry_url.get())
    # 已经是直链
    if 'download.aspx' in entry_url.get():
        label_directlink.config(text=entry_url.get())
        pyperclip.copy(entry_url.get())
        pyperclip.paste()
    # 判误
    elif result:
        directUrl = transferObj.fileDownloading()
        label_directlink.config(text=directUrl)
        pyperclip.copy(directUrl)
        pyperclip.paste()
    else:
        messagebox.showerror(title='错误', message='请输入正确的链接')


def imgHosting():
    label_directlink.config(text='')
    result = pattern in entry_url.get()
    if result == False:
        messagebox.showerror(title='错误', message='请输入正确的链接')
    else:
        label_tip.config(text='链接重定向中...')
        UrlRedirecctThread().start()


# 设置 Button
btn_download = tkinter.Button(win, text='下载直链', command=(lambda: fileDownloading()))
btn_download.place(relx=0.3, rely=0.65, relwidth=0.15, relheight=0.075)
btn_img = tkinter.Button(win, text='图床直链', command=(lambda: imgHosting()))
btn_img.place(relx=0.55, rely=0.65, relwidth=0.15, relheight=0.075)

label_hint = tkinter.Label(win, justify='left')
label_hint.config(text='●仅支持Onedrive for Business的单文件链接\n●“图床直链”需要先重定向链接，转换时间取决于网络状况\n●链接自动粘贴到剪切板')
label_hint.place(relx=0.01, rely=0.75, relwidth=0.5, relheight=0.2)

label_author = tkinter.Label(win, text='@荒唐的杰尼', fg='#E6E6E6')
label_author.place(relx=0.88, rely=0.95, relwidth=0.12, relheight=0.05)

# 进入消息循环
win.mainloop()
