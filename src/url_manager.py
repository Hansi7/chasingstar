from bs4 import BeautifulSoup
from bs4 import Tag
from sqlalchemy import desc
import requests
from DBcontext import DbEngine, Url
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.,2',
    'Accept-Encoding': 'gzip, deflate'
}

URL = 'https://www.javbus.com'
back_urls_txt = 'urls.txt'


class UrlManager:
    def __init__(self):
        self.dbsession = DbEngine().DBSession()

    def _update_url_from_web(self, _url='https://www.javbus.com'):
        try:
            wb_data = requests.get(_url, headers=headers, timeout=3)
        except TimeoutError:
            return []
        # with open('demo.html', 'r', encoding='utf8') as html:
        if wb_data.text:
            html = wb_data.text
            soup = BeautifulSoup(html, features='html.parser')
            ourl = soup.select(
                'body > div.container-fluid > div > div.alert.alert-info.alert-dismissable.alert-common > div > div')

            ourl = BeautifulSoup(str(ourl), features='html.parser')
            aourls = ourl.select('a')
            urls = []
            for a in aourls:
                assert isinstance(a, Tag)
                new_urls = a.get('href')
                urls.append(new_urls)
            urls.remove('https://www.javbus.com')
            return urls

    def _get_new_url_from_file(self):
        return self.dbsession.query(Url).order_by(desc('id'))[0:3]

    def update(self):
        """从表中读取旧的URL，从旧的URL中找到新的URL，并存入数据库。第一次运行时数据库为空，请先运行first_run"""
        source_urls = self.dbsession.query(Url).order_by(desc('id'))[0:3]

        for source_url in source_urls:
            urls = self._update_url_from_web(source_url.url)
            if len(urls) > 1:
                break

        print('updating urls...')
        print('Back Urls:')
        with open('urls.txt', 'w', encoding='utf8') as f:
            for u in urls:
                f.write(u + '\n')
                u_exist = self.dbsession.query(Url).filter(Url.url == u).all()
                if len(u_exist) == 0:
                    self.dbsession.add(Url(url=u, date=time.strftime("%Y-%m-%d")))
                print(u)
            self.dbsession.commit()
            self.dbsession.close()

    def show(self):
        urls = self._get_new_url_from_file()
        return urls

    def first_run(self):
        """第一次运行的时候，新建数据库和插入Url表数据"""
        urls = self._update_url_from_web()
        for u in urls:
            self.dbsession.add(Url(url=u, date=time.strftime("%Y-%m-%d")))
        self.dbsession.commit()
        self.dbsession.close()


if __name__ == '__main__':
    url_manager = UrlManager()
    # url_manager.first_run()
    url_manager.update()
    url_manager.show()
