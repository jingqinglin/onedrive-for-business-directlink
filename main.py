# coding:utf-8
import tkinter
from tkinter import ttk
from tkinter import messagebox
import pyperclip
import requests
import threading
import entryplaceholder
import directlink


class UrlRedirecctThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        redirectUrl = requests.get(entry_url.get()).url
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


win = tkinter.Tk()
win.iconbitmap('OneDrive.ico')
win.title('OneDrive for Business 直链')

# 修改了 python.exe/pythonw.exe 的 dpi 设置，以兼容高分屏
# https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp
h = win.winfo_screenheight() / 2.0
w = win.winfo_screenwidth() / 2.0
win.geometry(("%dx%d+%d+%d" % (w, h, w / 2, h / 2)))

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
label_directlink = tkinter.Label(frame_directlink, justify='left', wraplength=w * 0.95)
label_directlink.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.90)

label_tip = tkinter.Label(win, justify='left')
label_tip.place(relx=0.01, rely=0.6, relwidth=0.15, relheight=0.1)


def fileDownloading():
    result = pattern in entry_url.get()
    transferObj = directlink.TransferToDirectlink(entry_url.get())
    # 已经是直链
    if '_layouts/52/download.aspx?share=' in entry_url.get():
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

label_author = tkinter.Label(win, text='@JingqingLin', fg='gray')
label_author.place(relx=0.4, rely=0.95, relwidth=0.2, relheight=0.05)

# 进入消息循环
win.mainloop()
