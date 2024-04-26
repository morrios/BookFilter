import os
import re
import time
from multiprocessing.dummy import Pool
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from book_model import Book
from book_url import BookUrlHandle
from bookDetail import BookDetail
from chapter import getChapterContent


class FilterBook:
    bookContent = {}
    pool = Pool(10)
    chaptersCount = 0
    book = Book()
    chapter_down_error_list = []
    book_url_base = ""

    def __init__(self, base_url):
        self.bookDetail = None
        self.baseUrl = base_url
        self.handle = BookUrlHandle(base_url)
        self.findBook(base_url)

    def find_detail(self, soup):
        self.bookDetail = BookDetail(soup)
        self.book.bookName = self.bookDetail.getBookName()
        self.book.introduction = self.bookDetail.getBookDes()
        self.book.author = self.bookDetail.getBookAuthor()
        print("书名：", self.book.bookName)
        print("简介：", self.book.introduction)
        print("作者：", self.book.author)

    def findBook(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
        }
        request = requests.get(url=url, headers=headers)
        charset = self.pick_charset(request.text)
        if charset is not None:
            request.encoding = charset
        soup = BeautifulSoup(request.text, "html.parser")
        self.find_detail(soup)
        print("找到书籍《{}》".format(self.book.bookName))
        # 获取所有的章节
        chapters = self.bookDetail.getAllChapter()
        self.chaptersCount = len(chapters)
        chapter_data_list = []
        for index, chapter in enumerate(chapters):
            dic = {"index": index, "chapter": chapter}
            chapter_data_list.append(dic)
        # 执行map，传入列表
        self.pool.map(self.downloadPage, chapter_data_list)
        while len(self.chapter_down_error_list):
            self.pool.map(self.downloadPage, self.chapter_down_error_list)
        self.pool.close()
        self.pool.join()
        fopen = open(self.book.filePath, "a")
        fopen.write(self.book.bookName + "\n" * 3)
        fopen.write(self.book.detail + "\n")
        fopen.write(self.book.introduction + "\n" * 3)
        for index in range(len(chapter_data_list)):
            page = self.bookContent[index]
            fopen.write(page)
        fopen.close()
        print("一共{}章".format(len(chapters)))
        print("本书籍下载完成", end="\r")
        self.book.transBook()
        os.system("open %s" % (os.getcwd()))

    def pick_charset(self, html):
        """
        从文本中提取 meta charset
        :param html:
        :return:
        """
        charset = None
        m = re.compile(
            '<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I
        ).search(html)
        if m and m.lastindex == 2:
            charset = m.group(2).lower()
        return charset

    def test_pri(self, value):
        print(value)

    def downloadPage(self, chapterDict):
        index = chapterDict["index"]
        chapter = chapterDict["chapter"]
        if chapter is None:
            self.bookContent[index] = ""
            return index
        # pageTuple = self.filterChapter(index, chapter)
        herf = chapter["href"]
        page_url = self.handle.get_book_complete_url(herf)
        pageTuple = getChapterContent(index, page_url, chapter)

        if pageTuple[0] is True:
            self.bookContent[index] = pageTuple[1]
            if chapterDict in self.chapter_down_error_list:
                self.chapter_down_error_list.remove(chapterDict)
        else:
            self.chapter_down_error_list.append(chapterDict)
        process = (len(self.bookContent) / self.chaptersCount) * 100.0
        print(round(process, 1), end="\r")
        return index
