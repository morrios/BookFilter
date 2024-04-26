# encoding:utf-8

# 去除空格
def removeSpace(value):
    return ''.join(str(value).split())


class BookDetail:
    def __init__(self, soup):
        self.soup = soup
        self.bookDetail = self.soup.find('div', id='info')
        if not self.bookDetail:
            self.bookDetail = self.soup.find('div', class_='info')
        if not self.bookDetail:
            self.bookDetail = self.soup.find('div', class_='bookbox')
    def getBookName(self):
        return self.soup.find('h1').string

    def getBookAuthor(self):
        for child in self.bookDetail.descendants:
            if child is not None and child.string is not None and len(child.string.strip()) > 0:
                value = removeSpace(child.string)
                if '作者' in value:
                    return value
        return ""

    def findCover(self):
        fMimg = self.soup.find('div', id='fmimg')
        if not fMimg:
            fMimg = self.soup.find('div', class_='fmimg')
        img = fMimg.find('img')
        return img

    def getBookDes(self):
        des = self.soup.find('div', id='intro')
        if not des:
            des = self.soup.find('div', class_='intro')
        if des is None:
            return ''
        return des.get_text().strip()

    def getAllChapter1(self):
        chapters = []
        listmain = self.soup.body.find('div', class_='listmain')
        list_soup = listmain.find_all('dd')
        if not list_soup:
            list_soup = listmain.find_all('li')
        if not list_soup:
            list_soup = listmain.find_all('ul')
        chapters_dict = {}
        for index, item in enumerate(list_soup):
            a_tag = item.a
            if a_tag is not None and 'html' in a_tag['href']:
                chapters.append(item.a)
                print(item.get_text().strip())
            if index == 10:
                break
        return chapters

    def getAllChapter(self):
        chapters = []
        list_soup = self.soup.body.find_all('dd')
        if not list_soup:
            list_soup = self.soup.find_all('li')
        if not list_soup:
            list_soup = self.soup.find_all('ul')
        chapters_dict = {}
        for index, item in enumerate(list_soup):
            a_tag = item.a
            if a_tag is not None and 'html' in a_tag['href']:
                if item.parent in chapters_dict:
                    chapters_dict[item.parent].append(item.a)
                else:
                    chapters_dict[item.parent] = [item.a]
        for values in chapters_dict.values():
            if len(values) > len(chapters):
                chapters = values
        return chapters



