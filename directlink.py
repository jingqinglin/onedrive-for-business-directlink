class TransferToDirectlink():
    def __init__(self, url=''):
        if url == '请输入或粘贴正确的链接':
            self.url = ''
        else:
            self.url = url
        self.directlink = ''

    def img_hosting(self):
        split_str = self.url.split('%2F')
        head_str = split_str[0].split('/_')
        self.directlink += head_str[0]

        for index in range(len(split_str)):
            if index > 2:
                self.directlink += '/' + split_str[index]

        temp_link = self.directlink.split('&')
        self.directlink = temp_link[0]
        return self.directlink

    def file_downloading(self):
        if 'onedrive.aspx?id=' in self.url:
            split_str = self.url.split('onedrive.aspx?id=')
            self.directlink = split_str[0] + 'download.aspx?SourceUrl='
            split_sub_str = split_str[1].split('&parent=')
            self.directlink += split_sub_str[0]
        else:
            split_str = self.url.split('/')

            token_str = split_str[-1].split('?')
            add_str = '_layouts/52/download.aspx?share='

            for index in range(len(split_str)):
                if (index == len(split_str) - 1):
                    self.directlink = self.directlink + add_str + token_str[0]
                elif (index == len(split_str) - 4 or index == len(split_str) - 5):
                    pass
                else:
                    self.directlink = self.directlink + split_str[index] + '/'
        return self.directlink