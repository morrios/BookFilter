from urllib.parse import urlparse, urljoin


class BookUrlHandle:
    # 新的base地址
    book_url_base = ''

    def __init__(self, base_url):
        self.baseUrl = base_url

    def get_book_complete_url(self, book_url):
        if book_url.startswith('https://') or book_url.startswith('http://'):
            return book_url
        if len(self.book_url_base) == 0:
            self.book_url_base = self.merge_new_base_path(book_url)
        if book_url.startswith('/'):
            return self.merge_urls(self.baseUrl, book_url)
        return self.book_url_base + '/' + book_url

    def merge_urls(self, base_url, relative_url):
        # 解析基地址和相对地址
        parsed_base_url = urlparse(base_url)
        parsed_relative_url = urlparse(relative_url)
        # 拼接最终的URL
        final_url = urljoin(parsed_base_url.scheme + "://" + parsed_base_url.netloc, parsed_relative_url.path)
        return final_url

    def get_web_scheme(self):
        parsed_url = urlparse(self.baseUrl)
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc
        scheme = scheme + "://" + netloc
        return scheme

    def merge_new_base_path(self, book_url):
        base_path = urlparse(self.baseUrl).path
        base_path_array = [segment for segment in base_path.split('/') if segment]
        book_path = urlparse(book_url).path
        book_path_array = [segment for segment in book_path.split('/') if segment]
        merge_paths = self.remove_duplicate(base_path_array, book_path_array)
        merge_paths.insert(0, self.get_web_scheme())
        result_string = '/'.join(merge_paths)
        return result_string

    def remove_duplicate(self, array1, array2):
        unique_elements = set()
        result_array1 = []
        for element in array1:
            if element not in array2 and element not in unique_elements:
                result_array1.append(element)
                unique_elements.add(element)
        return result_array1
