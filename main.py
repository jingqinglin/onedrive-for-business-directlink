# coding:utf-8
import tkinter
from tkinter import ttk
import pyperclip
import entryplaceholder
import directlink

win = tkinter.Tk()
win.title('OneDrive for Business 直链')

# 修改了 python.exe/pythonw.exe 的 dpi 设置，以兼容高分屏
# https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp
h = win.winfo_screenheight() / 2.0
w = win.winfo_screenwidth() / 2.0
win.geometry(("%dx%d" % (w, h)))

frame_oriStr = ttk.LabelFrame(win, text="原链接", labelanchor="nw")
# rel 代表 relative
frame_oriStr.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.2)

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
frame_directlink.place(relx=0.01, rely=0.25, relwidth=0.98, relheight=0.3)
label_directlink = tkinter.Label(frame_directlink)
label_directlink.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.90)

transferObj = directlink.TransferToDirectlink(entry_url.get())


def fileDownloading():
    directUrl = transferObj.fileDownloading()
    label_directlink.config(text=directUrl)


def imgHosting():
    directUrl = transferObj.imgHosting()
    label_directlink.config(text=directUrl)


# 设置 Button
btn_download = tkinter.Button(win, text='下载直链', command=(lambda: fileDownloading()))
btn_download.place(relx=0.3, rely=0.65, relwidth=0.15, relheight=0.075)
btn_img = tkinter.Button(win, text='图床直链', command=(lambda: imgHosting()))
btn_img.place(relx=0.55, rely=0.65, relwidth=0.15, relheight=0.075)

# 进入消息循环
win.mainloop()
