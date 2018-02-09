from src.provider import Provider


class HocVienTruyenTranhCom(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/chapter/(\d+)', self.get_current_chapter())
        return '{}-{}'.format(self._chapter_index(), idx.group(1))

    def _test_main_url(self, url):
        if self.re.search('/chapter/', url):
            url = self.html_fromstring(url, '#subNavi a', 0).get('href')
        return url

    def get_main_content(self):
        url = self._test_main_url(self.get_url())
        return self.http_get(self.http().normalize_uri(url))

    def get_manga_name(self) -> str:
        url = self._test_main_url(self.get_url())
        return self.re.search('/manga/[^/]+/([^/]+)', url).group(1)

    def get_chapters(self):
        c, s = self.get_storage_content(), '.table-scroll table.table td > a'
        return self.document_fromstring(c)

    def get_files(self):
        selector = '.manga-container img.page'
        items = self.html_fromstring(self.get_current_chapter(), selector)
        return [i.get('src') for i in items]

    def get_cover(self):
        return self._get_cover_from_content('.__info-container .__image img')


main = HocVienTruyenTranhCom
