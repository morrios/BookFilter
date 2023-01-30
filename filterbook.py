import os
import threading
import time
import requests
from bs4 import BeautifulSoup
import unicodedata as ucd
from multiprocessing.dummy import Pool
class FilterBook:
    sites = ['笔趣阁','天籁小说']
    save_local_path = '/Users/dulinwei/Desktop/'
    chapterStart = '第一章'
    bookContent = {}
    pool = Pool(6)
    def __init__(self, baseUrl, bookIndex):
        self.baseUrl = baseUrl
        self.bookIndex = bookIndex
        self.findBook(baseUrl + bookIndex)
        

    def find_chapters(self, soup):
        boxCon = soup.find('div', id = 'list')
        tags = boxCon.find_all('a')
        startIndex = 0
        for index,tag in enumerate(tags):
            if(self.chapterStart in tag.string):
                startIndex = index
                break
        chapters = tags[startIndex:]
        return chapters

    def find_detail(self, soup):
        bookdetail = soup.find('div', id = 'info')
        des = soup.find('div', id = 'intro')
        book_name = bookdetail.find('h1')
        info_dic = {}
        info_dic['bookName'] = book_name.get_text().strip()
        info_dic['des'] = des.get_text().strip()
        detail_str = ''
        for child in bookdetail.children:
            detail_str = detail_str + child.get_text().strip() + '\n'
        info_dic['detail'] = detail_str
        return info_dic

    def filterChapter(self, chapter):
        paragraphs = ''
        herf = chapter['href']
        chapter_name = chapter.string
        page_url = self.baseUrl + herf
        html = requests.get(page_url)
        soup = BeautifulSoup(html.text, 'lxml')
        content = soup.find('div', id = 'content')
        paragraphs = chapter_name+'\n\n\n'
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
        if('chaptererror' in w):
            return False
        if(len(w) == 0):
            return False
        return True

    #存储书籍文件夹路径    
    def saveBookPath(self, bookName):
        book_dir = self.save_local_path + bookName
        if(not os.path.exists(book_dir)):
            os.mkdir(book_dir)
        return book_dir

    def savepath(self, bookName):
        return self.saveBookPath(bookName) + bookName + '.txt'

    def findBook(self, url):
        start_time = time.time()
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        book_info = self.find_detail(soup)
        book_name = book_info['bookName']
        print('找到书籍《{}》'.format(book_name))
        book_des = book_info['des']
        book_detail = book_info['detail']
        #获取所有的章节
        chapters = self.find_chapters(soup)
        chapter_data_list = []
        for index,chapter in enumerate(chapters):
            dic = {'index': index, 'chapter': chapter}
            chapter_data_list.append(dic)
        # 执行map，传入列表
        res_list = self.pool.map(self.downloadPage, chapter_data_list)
        print(res_list)
        self.pool.close()
        self.pool.join()
        fopen = open(self.savepath(book_name),"a")
        fopen.write(book_name + '\n'*3)
        fopen.write(book_des + '\n')
        fopen.write(book_detail + '\n'*5)
        for index in range(len(chapters)):
            page = self.bookContent[index]
            fopen.write(page)
        fopen.close()
        print('本书籍下载完成')

    def downloadPage(self, chapterDict):
        index = chapterDict['index']
        chapter = chapterDict['chapter']
        page = self.filterChapter(chapter)
        self.bookContent[index] = page
        return index

