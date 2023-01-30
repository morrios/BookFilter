# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import re
import time
import requests
from bs4 import BeautifulSoup
import unicodedata as ucd

chapterStart = '第一章'
baseUrl = 'https://www.tianlaibook.com/'
bookIndex = '200_200061/'
sites = ['天']
save_local_path = '/Users/dulinwei/Desktop/'
def find_chapters(soup):
    boxCon = soup.find('div', id = 'list')
    tags = boxCon.find_all('a')
    startIndex = 0
    for index,tag in enumerate(tags):
        if(chapterStart in tag.string):
            startIndex = index
            break
    chapters = tags[startIndex:]
    return chapters

def find_detail(soup):
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

def filterChapter(chapter):
    paragraphs = []
    herf = chapter['href']
    chapter_name = chapter.string
    page_url = baseUrl + herf
    html = requests.get(page_url)
    soup = BeautifulSoup(html.text, 'lxml')
    content = soup.find('div', id = 'content')
    paragraphs.append(chapter_name+'\n\n\n')
    for child in content.children:
        session = child.get_text().strip()
        if(not exclude_words(session)):
            continue
        if(session is not None):
            session = ucd.normalize('NFKC', session).replace(' ', '') 
            paragraphs.append(session + '\n\n')
    return paragraphs

#排除一些无用句子
def exclude_words(w):
    if('chaptererror' in w):
        return False
    if(len(w) == 0):
        return False
    return True

#存储路径    
def savepath(bookName):
    suffix = '.txt'
    return save_local_path + bookName + suffix

def findBook(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    book_info = find_detail(soup)
    book_name = book_info['bookName']
    print('找到书籍《{}》'.format(book_name))
    book_des = book_info['des']
    book_detail = book_info['detail']
    #获取所有的章节
    chapters = find_chapters(soup)
    fopen = open(savepath(book_name),"a")
    fopen.write(book_name + '\n'*3)
    fopen.write(book_des + '\n')
    fopen.write(book_detail + '\n'*5)
    chapters_count = len(chapters)
    for index,chapter in enumerate(chapters):
        page = filterChapter(chapter)
        #写入文件
        fopen.writelines(page) 
        print("%.2f" % (index / chapters_count * 100) + "%", end='\r')
    fopen.close()
    print('本书籍下载完成')
    
start_time = time.time()
findBook(baseUrl + bookIndex)
end_time = time.time()
print("一共耗时{}".format(end_time-start_time))