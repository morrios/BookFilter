# encoding:utf-8

class BookCatalogue:
    def __init__(self, soup):
        self.soup = soup

    # 零点读书：
    # 1. 分页
    # 2. 章节列表最上方都是最新章节
    def getAllChapter(self):
        chapters = []
        list_sec = self.soup.body.find_all('div', class_='section-box')
        if len(list_sec) < 2:
            return
        section = list_sec[1]
        list_a = section.find_all('a')
        sec_chapters = self.getAllChapter2(list_a)
        if sec_chapters:
            chapters.extend(sec_chapters)
        return chapters

    def getAllChapter2(self, a_list):
        chapters = []
        for index, item in enumerate(a_list):
            a_tag = item
            if a_tag is None:
                print(a_tag)
                continue
            if item.has_attr('href') and 'html' in item['href']:
                chapters.append(item)
            else:
                print("Not exist")
        return chapters
