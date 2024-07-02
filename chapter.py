import re

import requests
from bs4 import BeautifulSoup

from filter_config import keyWorkds

# 判断是否是 NoneType
def is_none_type(obj):
    return isinstance(obj, type(None))


def getChapterContent(index, page_url, chapter):
    chapter_name = chapter.string
    try:
        html = requests.get(page_url)
        # html.encoding = 'gbk'
        new_html = html.text.replace('<br/>', '\n')
        new_html = new_html.replace('<br>', '\n')
    except Exception as e:
        print('页面请求异常地址：' + page_url)
        print('再试一次')
        return False, ''
    soup = BeautifulSoup(new_html, 'html.parser')
    content = soup.find('div', id='content')
    if not content:
        content = soup.find('div', id='chaptercontent')

    if not content:
        print("获取内容失败")
        return False, ''
    paragraphs = get_chapter_name(index, chapter_name)
    try:
        for index, child in enumerate(content.children):
            session = child.get_text()
            if index == 0 and remove_space(session) == remove_space(chapter_name):
                continue
            if not exclude_words(session):
                continue
            new_line = get_new_line(session)
            if len(new_line) > 0:
                paragraphs = paragraphs + new_line + '\n\n'
    except Exception as e:
        print(paragraphs + '发生了异常\n' + '异常页面地址：' + page_url)
        print(e)
        return False, ''
    return True, paragraphs


def remove_space(text):
    return text.strip().replace(' ', '')


def get_new_line(text):
    if text is not None:
        session = ''.join(str(text).split())
        if len(session) > 0:
            return session
    return ''


def get_chapter_name(index, chapter_string):
    chapter_name = ''
    if re.search(r'第(.*?)章', chapter_string, re.M | re.I):
        chapter_name = chapter_string + '\n\n'
    elif re.match(r'^(\d+)[^\d]*', chapter_string):
        # 如果有数字前缀，则进行替换
        match = re.match(r'^(\d+)[^\d]*', chapter_string)
        chapter_number = match.group(1)
        paragraphs = re.sub(r'^\d+', f'第{chapter_number}章', chapter_string)
        chapter_name = paragraphs + '\n\n'
    else:
        chapter_name = '第' + str(index + 1) + '章' + ' ' + chapter_string + '\n\n'
    return chapter_name


# 如果是这样的章节：973.史上最大规模空战
def replace_num_chapter(text):
    # 判断是否有数字前缀
    match = re.match(r'^(\d+)[^\d]*', text)
    if match:
        # 如果有数字前缀，则进行替换
        chapter_number = match.group(1)
        replaced_text = re.sub(r'^\d+', f'第{chapter_number}章', text)
        return replaced_text
    else:
        # 如果没有数字前缀，不进行替换
        return text


def exclude_words(w):
    for key in keyWorkds:
        if key in w:
            return False
    if w is None:
        return False
    if len(w.replace(' ', '')) == 0:
        return False
    return True
