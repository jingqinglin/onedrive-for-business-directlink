# coding:utf-8
import ctypes
import math
import os
import re
import sys
import threading
import tkinter
from tkinter import messagebox
from tkinter import ttk

import pyperclip
import requests
import win32con
import win32gui
import win32print

import entryplaceholder

# 重定向并获取网页内容
class UrlRedirectThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        redirect_url, html = get_html(entry_url.get())
        direct_link = get_url_from_html(html)
        label_tip.config(text='直链已粘贴到剪贴板', fg='#ff5c6c')
        short_result_url = direct_link.split('access_token')[0] + 'acess_token=...'
        label_directlink.config(text=short_result_url)
        pyperclip.copy(direct_link)
        pyperclip.paste()

# 获取 html 内容
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    s = requests.Session()
    response = s.get(url, headers=headers)
    return response.url, response.text

# 由于 div 是动态加载的，爬取的 html 中没有图片链接，需要提取一下
def get_url_from_html(html):
    # mail.ustc.edu.cn 域的数据中心在欧洲/英国
    # https://ukwest1-mediap.svc.ms/
    media_base_url_ori = re.findall('mediaBaseUrl".+?\.ms', html)
    media_base_url = 'https://' + media_base_url_ori[0].split('u002f')[2] + '/'

    # 备选数据中心 https://uksouth1-mediap.svc.ms/
    media_base_url_secondary_ori = re.findall('mediaBaseUrlSecondary".+?\.ms', html)
    media_base_url_secondary = 'https://' + media_base_url_secondary_ori[0].split('u002f')[2] + '/'

    provider_ori = re.findall('\?provider.+&i', html)
    provider = provider_ori[0].split('=')[1].split('&')[0]

    file_type_ori = re.findall('%2E.[a-z|A-Z]+&', html)
    file_type = file_type_ori[0].split('&')[0].split('2E')[1]

    caller_stack_ori = re.findall('callerStack" : ".+[a-z|A-Z]', html)
    caller_stack = caller_stack_ori[0].split('"')[2]

    current_folder_sp_item_url_ori = re.findall('CurrentFolderSpItemUrl.+', html)
    current_folder_sp_item_url = current_folder_sp_item_url_ori[0].split('"')[2]

    access_token_ori = re.findall('driveAccessToken":"access_token.+","', html)
    access_token = access_token_ori[0].split('"')[2].split('=')[1]

    result_url = media_base_url + 'transform/thumbnail?provider=' + provider + \
                    '&inputFormat=' + file_type + '&cs=' + caller_stack + '&docid=' + current_folder_sp_item_url + \
                    '&access_token=' + access_token + '&encodeFailures=1&srcWidth=&srcHeight=&width=' + \
                    str(HORZRES) + '&height=' + str(VERTRES / 2) + '&action=Access'
    return result_url

# 修正 ico 图标路径
# https://blog.csdn.net/you227/article/details/46989625
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        print(os.path.join(sys._MEIPASS, relative))
        return os.path.join(sys._MEIPASS, relative)
    print('relative: ' + os.path.join(relative))
    return os.path.join(relative)

# 获取屏幕 dpi
def get_dpi():
    MM_TO_IN = 1 / 25.4
    pxw = math.sqrt(pow(HORZRES, 2) + pow(VERTRES, 2))
    inw = math.sqrt(pow(win.winfo_screenmmwidth(), 2) + pow(win.winfo_screenmmheight(), 2)) * MM_TO_IN
    return pxw / inw

def process_file_downloading(url):
    result_url = ''
    if 'onedrive.aspx?id=' in url:
        split_str = url.split('onedrive.aspx?id=')
        result_url = split_str[0] + 'download.aspx?SourceUrl='
        split_sub_str = split_str[1].split('&parent=')
        result_url += split_sub_str[0]
    else:
        split_str = url.split('/')
        token_str = split_str[-1].split('?')
        add_str = '_layouts/52/download.aspx?share='
        for index in range(len(split_str)):
            if (index == len(split_str) - 1):
                result_url += add_str + token_str[0]
            elif (index == len(split_str) - 4 or index == len(split_str) - 5):
                pass
            else:
                result_url += split_str[index] + '/'
    return result_url

def file_download_button():
    is_onedrivelink = pattern in entry_url.get()
    # 已经是直链
    if download_pattern in entry_url.get():
        label_directlink.config(text=entry_url.get())
        pyperclip.copy(entry_url.get())
        pyperclip.paste()
        label_tip.config(text='直链已粘贴到剪贴板', fg='#ff5c6c')
    # 判误
    elif '/:f:/g' in entry_url.get() and is_onedrivelink:
        messagebox.showerror(title='错误', message='不支持文件夹链接')
    elif is_onedrivelink:
        direct_link = process_file_downloading(entry_url.get())
        label_directlink.config(text=direct_link)
        pyperclip.copy(direct_link)
        pyperclip.paste()
        label_tip.config(text='直链已粘贴到剪贴板', fg='#ff5c6c')
    else:
        messagebox.showerror(title='错误', message='请输入正确的链接')

def img_host_button():
    label_directlink.config(text='')
    is_onedrivelink = pattern in entry_url.get()
    if is_onedrivelink == False:
        messagebox.showerror(title='错误', message='请输入正确的链接')
    elif redirect_pattern in entry_url.get():
        messagebox.showerror(title='错误', message='请输入未重定向的链接')
    elif download_pattern in entry_url.get():
        messagebox.showerror(title='错误', message='请输入正确的链接')
    elif '/:f:/g' in entry_url.get():
        messagebox.showerror(title='非图片链接', message='不支持文件夹链接')
    elif '/:v:/g' in entry_url.get() or '/:u:/g' in entry_url.get():
        messagebox.showerror(title='非图片链接', message='不支持音视频链接，请选择“下载直链”')
    elif '/:i:/g' not in entry_url.get():
        messagebox.showerror(title='非图片链接', message='请输入图片链接或选择“下载直链”')
    else:
        label_tip.config(text='链接正在重定向…', fg='#ff5c6c')
        UrlRedirectThread().start()

# ----------------------------------画窗口----------------------------------#
# 主窗口
win = tkinter.Tk()
ico_path = resource_path(r'./OneDrive.ico')
if os.path.exists(ico_path):
    win.iconbitmap(ico_path)
win.title('OneDrive for Business 直链')

# 窗口分辨率及位置设置
# https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp
# win.winfo_screenheight() & win.winfo_screenwidth() 会根据 Windows 缩放比例变化，无法计算正确的 dpi
# 参考 https://www.cnblogs.com/micenote/p/12165669.html 获取屏幕分辨率
hDC = win32gui.GetDC(0)
# 横向分辨率
HORZRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
# 纵向分辨率
VERTRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
# PROCESS_DPI_UNAWARE            = 0,
# PROCESS_SYSTEM_DPI_AWARE       = 1,
# PROCESS_PER_MONITOR_DPI_AWARE  = 2
ctypes.windll.shcore.SetProcessDpiAwareness(1)
win.tk.call('tk', 'scaling', get_dpi() / 72)
win.geometry(("%dx%d+%d+%d" % (HORZRES / 2, VERTRES / 2, HORZRES / 4, VERTRES / 4)))

# 原链接 LabelFrame
frame_oriStr = ttk.LabelFrame(win, text="原链接", labelanchor="nw")
# rel 代表 relative
frame_oriStr.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.2)
# 获取剪贴板，设置 Entry 组件
clipboard = pyperclip.paste()
pattern = '-my.sharepoint.com/'
redirect_pattern = 'onedrive.aspx?'
download_pattern = 'download.aspx?'
is_onedrivelink = pattern in clipboard
if is_onedrivelink:
    entry_url = entryplaceholder.EntryWithPlaceholder(frame_oriStr, placeholder=clipboard, color='black')
else:
    entry_url = entryplaceholder.EntryWithPlaceholder(frame_oriStr, placeholder='请输入或粘贴正确的链接')
entry_url.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.90)

# 直链 LabelFrame
frame_directlink = ttk.LabelFrame(win, text="直链", labelanchor="nw")
frame_directlink.place(relx=0.01, rely=0.25, relwidth=0.98, relheight=0.3)
label_directlink = tkinter.Label(frame_directlink, justify='left', wraplength=win.winfo_screenwidth() * 0.95)
label_directlink.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

# 重定向时进行文字提示
label_tip = tkinter.Label(win, justify='left')
label_tip.place(relx=0.01, rely=0.55, relwidth=0.20, relheight=0.1)

# 设置 Button
btn_download = tkinter.Button(win, text='下载直链', command=(lambda: file_download_button()))
btn_download.place(relx=0.3, rely=0.64, relwidth=0.15, relheight=0.075)
btn_img = tkinter.Button(win, text='图床直链', command=(lambda: img_host_button()))
btn_img.place(relx=0.55, rely=0.64, relwidth=0.15, relheight=0.075)

label_hint = tkinter.Label(win, justify='left')
label_hint.config(text='● 仅支持 Onedrive for Business 的单文件链接\n● 获取“图床直链”需要先重定向链接，转换时间取决于网络状况\n● 链接自动粘贴到剪切板')
label_hint.place(relx=0.01, rely=0.80, relwidth=0.5, relheight=0.2)
label_author = tkinter.Label(win, text='@', fg='#E6E6E6')
label_author.place(relx=0.88, rely=0.95, relwidth=0.12, relheight=0.05)

# 进入消息循环
win.mainloop()
