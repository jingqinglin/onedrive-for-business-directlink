# OneDrive for Business 直链

OneDrive for Business 文件分享链接转直链，只适用于单个文件，文件夹分享无法生效

## 代码运行

- `pip install -r requirements.txt`
- `python main.py`

## 二进制文件
从 [release](https://github.com/JingqingLin/OneDrive-directlink/releases) 直接下载二进制文件
<br><br>
- 对于某些非正确格式的链接，可能不会判误

## 使用方法
选择 OneDrive 中文件，右键-共享

<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200130155810.png" width = "40%" height = "40%">

复制链接

<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200115000743.png" width = "40%" height = "40%">

### 图床直链
> 图床直链只适用于图片格式的文件

打开软件，点`图床直链`，链接自动复制到剪切板

<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200130153230.png" width = "70%" height = "70%">

粘贴链接到浏览器打开

<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200130153545.png" width = "70%" height = "70%">

### 下载直链
打开软件，点`下载直链`

<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200130153722.png" width = "70%" height = "70%">

粘贴链接到浏览器打开，弹出下载框

<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200115002131.png" width = "70%" height = "70%">

## 自行编译
- `pip install pyinstaller`
- `pyinstaller -F -w -i OneDrive.ico main.py -p entryplaceholder.py`
- 在 main.spec 中修改图标和程序名称，如下图
`[('.\\OneDrive.ico',icon_path,'DATA')],
          name='OneDrive for Business 转直链',`

<img src="https://cdn.jsdelivr.net/gh/jingqinglin/image-hosting/img/20220225140900.png">

- `pyinstaller -F -w main.spec`，将重新生成 .exe 文件