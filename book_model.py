import os
import requests
from urllib.parse import urlparse

class Book:
    #地址
    url = '' 
    #其他信息
    detail = ''
    #简介
    introduction = ''
    #章节目录
    chapters = ''
    #存储文件夹
    saveDir = ''
    #存储地址
    filePath = ''
    #封面图
    coverPath = ''
    
    #书名
    @property
    def bookName(self):
        return self._bookName

    @bookName.setter
    def bookName(self, value):
        self._bookName = value
        self.saveDir = self.saveBookPath(value)
        self.filePath = self.savePath(value)

    #存储书籍文件夹路径    
    def saveBookPath(self, bookName):
        book_dir = os.getcwd() + '/' + bookName
        if(not os.path.exists(book_dir)):
            os.mkdir(book_dir)
        return book_dir

    def savePath(self, bookName):
        return self.saveBookPath(bookName) + '/' +bookName + '.txt'

    def downCover(self, cover):
        a = urlparse(cover)
        file_name = os.path.basename(a.path)
        self.coverPath = self.saveDir + '/'  + file_name
        with open(self.coverPath, 'wb') as f:
            f.write(r.content)   

    def transBook(self):
        cli_str = 'kaf-cli -cover %s -filename %s' % (self.coverPath, self.filePath)
        if  not self.coverPath:
            cli_str = 'kaf-cli %s' % (self.filePath)
        print(cli_str)
        os.system(cli_str)