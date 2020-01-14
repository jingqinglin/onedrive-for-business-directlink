# OneDrive for Business 直链
 OneDrive for Business 文件分享链接转直链
 
<br><br>
## 使用方法
选择OneDrive中文件，右键-共享  
<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200114235558.png" width = "40%" height = "40%">  
-复制链接  
<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200115000743.png" width = "40%" height = "40%">  
### 图床直链
打开软件，点`图床直链`，链接自动复制到剪切板  
<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200115001650.png" width = "70%" height = "70%">  
粘贴链接到浏览器打开  
<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200115001837.png" width = "70%" height = "70%">  
### 下载直链
打开软件，点`下载直链`  
<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200115002023.png" width = "70%" height = "70%">  
粘贴链接到浏览器打开  
<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200115002131.png" width = "70%" height = "70%"> 

<br><br>
## 编译
> pip install pyinstaller  
 
> pyinstaller -F -w -i OneDrive.ico main.py -p entryplaceholder.py -p directlink.py  

修改main.spec，ico图标等资源打包到exe（指定绝对路径）  

<img src="https://cdn.jsdelivr.net/gh/JingqingLin/ImageHosting/img/20200115020541.png">  

> pyinstaller -F -w main.spec  

重新生成.exe文件
 

<br><br>
## 二进制文件
从 [release](https://github.com/JingqingLin/OneDrive-directlink/releases) 获取二进制文件
<br><br>
- 对于某些非正确格式的链接，可能不会判误
