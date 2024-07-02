# encoding:utf-8


# 去除空格
def removeSpace(value):
    return ''.join(str(value).split())


class BookDetail:
    def __init__(self, soup):
        self.soup = soup
        self.bookDetail = self.soup.find('div', id='info')
        if not self.bookDetail:
            print('No book detail found')
            self.bookDetail = self.soup.find('div', class_='info')
        if not self.bookDetail:
            self.bookDetail = self.soup.find('div', class_='bookbox')
        print(self.bookDetail)

    def getBookName(self):
        return self.bookDetail.find('h1').string

    def getBookAuthor(self):
        for child in self.bookDetail.descendants:
            if child is not None and child.string is not None and len(child.string.strip()) > 0:
                value = removeSpace(child.string)
                print("value:", value)
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
