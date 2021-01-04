#!/usr/bin/env python
# -*-coding:utf-8-*-

import downloader
import pageparser
from bs4 import BeautifulSoup
from url_manager import UrlManager
from DBcontext import DbEngine, Girl
import time
import functools

now = functools.partial(time.strftime, "%Y-%m-%d")

session = DbEngine().DBSession()


def girls_movie_by_id(id):
    girl = session.query(Girl).filter(Girl.id == id).one()
    return girls_movie(girl.scode)


def girls_movie(scode, maxpage=1):
    um = UrlManager()
    um.update()
    source_urls = um.show()
    url_to_scray = source_urls[0].url + '/star/' + scode
    print('url is ' + url_to_scray)
    html = downloader.get_html(url_to_scray)
    soup = BeautifulSoup(html, "html.parser")

    results = []

    nextpageurl = 'first_loop'
    page_counter = 0
    while nextpageurl != None:
        if nextpageurl != 'first_loop':  #
            html = downloader.get_html(nextpageurl)
            soup = BeautifulSoup(html, "html.parser")
        for url in pageparser.parser_homeurl(html):
            results.append(url)
        nextpageurl = pageparser.get_next_page_url(source_urls[0].url, html)
        page_counter += 1
        print('page => ' + str(page_counter))
        if page_counter == maxpage:
            break
    fcodes = []
    for url in results:
        print(url)
        code = (url[len(source_urls[0].url):]).strip('/')
        fcodes.append(code)
    return fcodes


def get_girls(girl_id=None):
    if not girl_id:
        return session.query(Girl).all()
    else:
        return session.query(Girl).filter(Girl.id == girl_id).all()


def unsubscribe_girl(id):
    ggg = session.query(Girl).filter(Girl.id == id).one()
    session.delete(ggg)
    session.commit()
    print('Unsubscribe success!')


def subscribe_girl(name, scode):
    gs = session.query(Girl).filter(Girl.scode == scode).all()
    if len(gs) == 0:
        session.add(Girl(name=name, scode=scode, date=now()))
        print(str(name) + 'subscribed!')
        session.commit()
        session.close()


def subscribe_girl(scode):
    gs = session.query(Girl).filter(Girl.scode == scode).all()
    if len(gs) == 0:
        uu = UrlManager().show()[0].url + '/star/' + scode
        html = downloader.get_html(uu)
        name = pageparser.parser_girlurl(html)
        session.add(Girl(name=str(name), scode=scode, date=now()))
        print(str(name) + 'subscribed!')
        session.commit()
        session.close()
    else:
        print('this girl already subscribed!')


if __name__ == '__main__':
    pass
    # scodes = ['okq', '1ny', 'pmv', '2yl', 'qfy', 'n5q', 'r62', 'p84', 'b64', '8ec', '86u', 'p71', '2di', 'mj2', 'b6a',
    #           'rgh', 'rmx', 'py1', 'rxf', 'sf0', 'snq', 'sba', 'o1a', 'sq2', 'sjk', 's1l', 's4p', 'squ', 'sl1', 't39',
    #           'two', 'tyv']
    # for scode in scodes:
    #     # girls_movie(scode)
    #     subscribe_girl(scode)
    # unsubscribe_girl(23)
