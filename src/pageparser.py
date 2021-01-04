#!/usr/bin/env python
# -*-coding:utf-8-*-

from bs4 import BeautifulSoup
import time
import downloader


def _parser_magnet(html):
    """parser_magnet(html),get all magnets from a html and return the str of magnet"""

    # 存放磁力的字符串
    magnet = ''
    soup = BeautifulSoup(html, "html.parser")
    for td in soup.select('td[width="70%"]'):
        magnet += td.a['href'] + '\n'
    return magnet


def parser_content(html):
    """parser_content(html),parser page's content of every url and yield the dict of content"""

    soup = BeautifulSoup(html, "html.parser")

    categories = {}

    code_name_doc = soup.find('span', text="識別碼:")
    code_name = code_name_doc.parent.contents[2].text if code_name_doc else ''
    categories['番号'] = code_name.strip()

    # 网址加入字典
    url = soup.select('link[hreflang="zh"]')[0]['href']
    categories['URL'] = url.strip()

    title = soup.select_one('a.bigImage').next['title']
    categories['标题'] = title.strip()

    date_issue_doc = soup.find('span', text="發行日期:")
    date_issue = date_issue_doc.parent.contents[1].strip() if date_issue_doc else ''
    categories['发行日期'] = date_issue.strip()
    # date_issue = soup.find('span', text="發行日期:").parent.contents[1].strip() if soup.find('span', text="發行日期:") else ''

    duration_doc = soup.find('span', text="長度:")
    duration = duration_doc.parent.contents[1].strip() if duration_doc else ''
    categories['长度'] = duration.strip()
    # duration = soup.find('span', text="長度:").parent.contents[1].strip() if soup.find('span', text="長度:") else ''

    director_doc = soup.find('span', text="導演:")
    director = director_doc.parent.contents[2].text if director_doc else ''
    categories['导演'] = director.strip()
    # director = soup.find('span', text="導演:").parent.contents[2].text if soup.find('span', text="導演:") else ''

    manufacturer_doc = soup.find('span', text="製作商:")
    manufacturer = manufacturer_doc.parent.contents[2].text if manufacturer_doc else ''
    categories['制作商'] = manufacturer.strip()
    # manufacturer = soup.find('span', text="製作商:").parent.contents[2].text if soup.find('span', text="製作商:") else ''

    publisher_doc = soup.find('span', text="發行商:")
    publisher = publisher_doc.parent.contents[2].text if publisher_doc else ''
    categories['发行商'] = publisher.strip()
    # publisher = soup.find('span', text="發行商:").parent.contents[2].text if soup.find('span', text="發行商:") else ''

    series_doc = soup.find('span', text="系列:")
    series = series_doc.parent.contents[2].text if series_doc else ''
    categories['系列'] = series.strip()
    # series = soup.find('span', text="系列:").parent.contents[2].text if soup.find('span', text="系列:") else ''

    actor_doc = soup.select('span[onmouseover^="hoverdiv"]')
    actor = (i.text.strip() for i in actor_doc) if actor_doc else ''
    # actor = (i.text.strip() for i in soup.select('span[onmouseover^="hoverdiv"]')) if soup.select('span[onmouseover^="hoverdiv"]') else ''
    actor_text = ''
    for tex in actor:
        actor_text += '%s   ' % tex
    categories['演员'] = actor_text.strip()

    genre_doc = soup.find('p', text="類別:")
    genre = (i.text.strip() for i in genre_doc.find_next('p').select('span')) if genre_doc else ''
    # genre =(i.text.strip() for i in soup.find('p', text="類別:").find_next('p').select('span')) if soup.find('p', text="類別:") else ''
    genre_text = ''
    for tex in genre:
        genre_text += '%s   ' % tex
    categories['类别'] = genre_text.strip()

    categories['封面'] = soup.select_one('.bigImage')['href']

    # 将磁力链接加入字典
    # mlinks = btdiggs.get_cili_by_fcode_btmayi(code_name.strip())
    # categories['磁力链接'] = '\n'.join(mlinks)

    # magnet_html = downloader.get_html(_get_cili_url(soup), Referer_url=url)
    # magnet = _parser_magnet(magnet_html)

    # categories['磁力链接'] = magnet
    categories['简介'] = ''
    categories['本地路径'] = ''

    categories['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    categories['无码'] = 0

    return categories


def get_next_page_url(sourceURL, html):
    """get_next_page_url(entrance, html),return the url of next page if exist"""
    print("...getting next page url...")
    soup = BeautifulSoup(html, "html.parser")
    next_page = soup.select('a[id="next"]')
    if next_page:
        next_page_link = next_page[0]['href']
        next_page_url = sourceURL + next_page_link
        return next_page_url
    return None


def parser_homeurl(html):
    """parser_homeurl(html),parser every url on every page and yield the url"""

    soup = BeautifulSoup(html, "html.parser")
    for url in soup.select('a[class="movie-box"]'):
        yield url['href']


def parser_girlurl(html: object) -> object:
    """
    return girls name
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.select_one('div.avatar-box>div>img')['title']
