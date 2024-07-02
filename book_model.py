import os
import subprocess
from idlelib.multicall import r

import requests
from urllib.parse import urlparse


class Book:
    # 地址
    url = ''
    # 其他信息
    detail = ''
    # 简介
    introduction = ''
    # 章节目录
    chapters = ''
    # 存储文件夹
    saveDir = ''
    # 存储地址
    filePath = ''
    # 封面图
    coverPath = ''
    # 作者
    author = ''

    # 书名
    def __init__(self):
        # 输出文件名，不需要包含格式后缀
        self.outPath = None
        # 书籍格式: all、epub、mobi、azw3,默认是all
        self.format = 'epub'

    @property
    def bookName(self):
        return self._bookName

    @bookName.setter
    def bookName(self, value):
        self._bookName = value
        self.saveDir = self.saveBookPath(value)
        self.filePath = self.savePath(value)
        self.outPath = self.saveOutPath(value)

    # 存储书籍文件夹路径
    def saveBookPath(self, book_name):
        book_dir = os.getcwd() + '/' + book_name
        if not os.path.exists(book_dir):
            os.mkdir(book_dir)
        return book_dir

    def savePath(self, book_name):
        return self.saveBookPath(book_name) + '/' + book_name + '.txt'

    def saveOutPath(self, book_name):
        return self.saveBookPath(book_name) + '/' + book_name

    def downCover(self, cover):
        a = urlparse(cover)
        file_name = os.path.basename(a.path)
        self.coverPath = self.saveDir + '/' + file_name
        with open(self.coverPath, 'wb') as f:
            f.write(r.content)

    def transBook(self):
        # kaf-cli  -format epub -filename /Users/dulinwei/Documents/kaf-cli/我在聊天群模拟长生路.txt -tips=0 -out /Users/dulinwei/Documents/kaf-cli/我在聊天群模拟长生路
        cli_str = 'kaf-cli -tips=0'
        if self.filePath:
            cli_str = '%s -filename %s' % (cli_str, self.filePath)
        if len(self.outPath) != 0:
            cli_str = '%s -out %s' % (cli_str, self.outPath)
        if len(self.author) != 0:
            cli_str = '%s -author %s' % (cli_str, self.author)
        # if len(self.format) != 0:
        cli_str = '%s -match "第.{1,8}章"' % (cli_str)
        print(cli_str)
        ret, val = subprocess.getstatusoutput(cli_str)
        print(ret)
        print(val)

