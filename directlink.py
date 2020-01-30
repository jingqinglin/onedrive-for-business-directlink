class TransferToDirectlink():
    def __init__(self, url=''):
        if url == '请输入或粘贴正确的链接':
            self.url = ''
        else:
            self.url = url
        self.directlink = ''

    # def imgHosting(self):
    #     splitStr = self.url.split('%2F')
    #     headStr = splitStr[0].split('/_')
    #     self.directlink += headStr[0]
    #
    #     for index in range(len(splitStr)):
    #         if index > 2:
    #             self.directlink += '/' + splitStr[index]
    #
    #     tempLink = self.directlink.split('&')
    #     self.directlink = tempLink[0]
    #     return self.directlink

    def fileDownloading(self):
        if 'onedrive.aspx?id=' in self.url:
            splitStr = self.url.split('onedrive.aspx?id=')
            self.directlink = splitStr[0] + 'download.aspx?SourceUrl='
            splitSubStr = splitStr[1].split('&parent=')
            self.directlink += splitSubStr[0]
        else:
            splitStr = self.url.split('/')

            tokenStr = splitStr[-1].split('?')
            addStr = '_layouts/52/download.aspx?share='

            for index in range(len(splitStr)):
                if (index == len(splitStr) - 1):
                    self.directlink = self.directlink + addStr + tokenStr[0]
                elif (index == len(splitStr) - 4 or index == len(splitStr) - 5):
                    pass
                else:
                    self.directlink = self.directlink + splitStr[index] + '/'
        return self.directlink
