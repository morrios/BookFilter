import os
import time
import requests
from bs4 import BeautifulSoup
import unicodedata as ucd
from multiprocessing.dummy import Pool
from book_model import Book
from filter_config import keyWorkds 
class FilterBook:
    chapterStart = ['第一章','第1章']
    bookContent = {}
    pool = Pool(10)
    chaptersCount = 0
    book = Book()
    def __init__(self, baseUrl, bookIndex):
        self.baseUrl = baseUrl
        self.bookIndex = bookIndex
        self.findBook(baseUrl + bookIndex)
        

    def find_chapters(self, soup):
        startIndex = 0
        boxCon = soup.find('div', id = 'list')
        dlCon = boxCon.find('dl')
        chapters = []
        for index, sub in enumerate(dlCon.children):
            if(self.book.bookName in sub.string and '最新章节' not in sub.string):
                startIndex = index
                break
        for index, sub in enumerate(dlCon.children):
            if(index > startIndex and sub.name is not None):
                chapters.append(sub.find('a'))
        return chapters

 

    def find_detail(self, soup):
        bookdetail = soup.find('div', id = 'info')
        des = soup.find('div', id = 'intro')
        book_name = bookdetail.find('h1')
        self.book.bookName = book_name.get_text().strip()
        self.book.introduction = des.get_text().strip()
        detail_str = ''
        for child in bookdetail.children:
            detail_str = detail_str + child.get_text().strip() + '\n'
        self.book.detail = detail_str

    def find_cover(self, soup):
        fmimg = soup.find('div', id = 'fmimg')
        img = soup.find('img')
        self.book.downCover(img['src'])
      
      
    def filterChapter(self, index, chapter):
        paragraphs = ''
        herf = chapter['href']
        chapter_name = chapter.string
        print(chapter_name + herf)
        page_url = self.baseUrl + herf
        html = requests.get(page_url)
        soup = BeautifulSoup(html.text, 'lxml')
        content = soup.find('div', id = 'content')
        paragraphs = '第' + str(index+1) +'章' + chapter_name+'\n\n\n'
        for child in content.children:
            session = child.get_text().strip()
            if(not self.exclude_words(session)):
                continue
            if(session is not None):
                session = ucd.normalize('NFKC', session).replace(' ', '')
                paragraphs = paragraphs + session + '\n\n';
        return paragraphs



    #排除一些无用句子
    def exclude_words(self, w):
        for key in keyWorkds:
            if(key in w):
                return False        
        if(len(w) == 0):
            return False
        if(self.book.bookName in w):
            return False
        return True

    def findBook(self, url):
        start_time = time.time()
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        self.find_detail(soup)
        # self.find_cover(soup)
        print('找到书籍《{}》'.format(self.book.bookName))
        #获取所有的章节
        chapters = self.find_chapters(soup)
        self.chaptersCount = len(chapters)
        chapter_data_list = []
        for index,chapter in enumerate(chapters):
            dic = {'index': index, 'chapter': chapter}
            chapter_data_list.append(dic)
        # 执行map，传入列表
        res_list = self.pool.map(self.downloadPage, chapter_data_list)
        self.pool.close()
        self.pool.join()
        fopen = open(self.book.filePath,"a")
        fopen.write(self.book.bookName + '\n'*3)
        fopen.write(self.book.detail + '\n')
        fopen.write(self.book.introduction + '\n'*3)
        for index in range(len(chapter_data_list)):
            page = self.bookContent[index]
            fopen.write(page)
        fopen.close()
        print('一共{}章'.format(len(chapters)));
        print('本书籍下载完成', end='\r')
        self.book.transBook()
        os.system('open %s'%(os.getcwd()))
        

    def downloadPage(self, chapterDict):
        index = chapterDict['index']
        chapter = chapterDict['chapter']
        page = self.filterChapter(index,chapter)
        self.bookContent[index] = page
        process = (len(self.bookContent) / self.chaptersCount) * 100.0
        print(round(process, 1), end='\r');
        return index

