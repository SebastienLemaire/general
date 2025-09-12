#!/home/slemaire/miniconda3/bin/python


"""
nature_news_views_rss.py
    Create RSS feed from the Nature "News & Views" articles

Usage:
    python nature_news_views_rss.py
"""

from bs4 import BeautifulSoup as bs
from urllib.request import (
    urlopen, urlparse, urlunparse, urlretrieve)
import os
import sys
import time
import subprocess
from github import Auth
from github import Github


def main():
    """Create RSS from website Nature News & Views"""
    # https://www.nature.com/nature/articles?type=news-and-views
    #
    ## retrieve articles
    item_list = retrieve_articles()
    #
    #
    ## print XML for RSS feed
    # tcrea = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    xmlt = make_rss_text(item_list)
    #
    #
    ## update the file
    update_file(xmlt)
    #
    # while True:
    #     #
    #     ## wait for a day before next update
    #     time.sleep(60 * 60 * 24)


def make_rss_text(item_list):
    xmlt = '''<?xml version='1.0' encoding='UTF-8'?>
        <rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
        <channel>
            <title>Nature News and Views</title>
            <link>https://github.com/SebastienLemaire/general/blob/main/nature_news_views.rss</link>
            <description>News and Views articles from Nature Publishing Group journals</description>
            <atom:link href="https://github.com/SebastienLemaire/general/blob/main/nature_news_views.rss" rel="self"/>
            <docs>http://www.rssboard.org/rss-specification</docs>
            <generator>nature_news_views_rss.py</generator>
            <language>en</language>
            <lastBuildDate>Tue, 12 Sep 2023 13:18:50 +0000</lastBuildDate>
            <pubDate>Sat, 09 Sep 2023 06:00:00 -0400</pubDate>
            <ttl>120</ttl>
    '''
    #
    #
    for item in item_list:
        xml_item = '''
            <item>
                <title>%s</title>
                <link>%s</link>
                <description>%s</description>
                <content:encoded><![CDATA[<div><p style="color: #4aa564;">%s</p></div>]]></content:encoded>
                <pubDate>%s</pubDate>
                %s
                <dc:date>%s</dc:date>
                <dc:source>%s</dc:source>
                <dc:title>%s</dc:title>
                <dc:identifier>doi:10.1038/%s</dc:identifier>
            </item>
        ''' % (item['item_title'], item['item_href'], item['item_summary'], item['item_summary'], item['temps'], item['item_author'], item['temps'], item['item_journal'], item['item_title'], item['item_doi'])
        #
        xmlt += xml_item
    #
    #
    xmlt +='''    
        </channel>
    </rss>
    '''
    #
    return(xmlt)


def update_file(xmlt):
    os.chdir('/mnt/c/Users/slemaire/softwares/')
    #
    #
    rss_path = '/mnt/c/Users/slemaire/softwares/general/nature_news_views.rss'
    with open(rss_path, 'w') as fich:
        print(xmlt, file = fich)
    #
    #
    # os.system('cd /mnt/c/Users/slemaire/softwares/general/')
    os.chdir('/mnt/c/Users/slemaire/softwares/general/')

    # os.system('git add nature_news_views.rss')
    # os.system('git commit -m "update"')
    # os.system('git push -u origin main')
    
    # Write contents to file in GitHub repo:
    toktxt="_pat_11ALYIFPA0exyGMhheoajy_ZmdbOnaKJT4mNr0HaklxG3LlNnKwNwOuxAORfwxMOc0KJ7UGAVPEYcw87pY"
    auth = Auth.Token("github" + toktxt)
    g = Github(auth=auth)
    repo = g.get_repo("SebastienLemaire/general")

    contents = repo.get_contents(path="nature_news_views.rss", ref="main")
    repo.update_file(path=contents.path, message="update RSS XML", content=xmlt, sha=contents.sha, branch="main")





def retrieve_articles(url_list=['https://www.nature.com/nature/articles?type=news-and-views', 'https://www.nature.com/ng/articles?type=news-and-views', 'https://www.nature.com/nm/articles?type=news-and-views', 'https://www.nature.com/ncb/articles?type=news-and-views', 'https://www.nature.com/nmeth/articles?type=news-and-views', 'https://www.nature.com/nplants/articles?type=news-and-views']):
    jdic = {
        'nature': 'Nature',
        'ng': 'Nature Genetics',
        'nm': 'Nature Medicine',
        'ncb': 'Nature Cell Biology',
        'nmeth': 'Nature Methods',
        'nplants': 'Nature Plants'
    }
    #
    item_list = []
    for url in url_list:
        url_sect = url.split('/')
        # domain = url.split('/')[2]
        url_base = '/'.join(url_sect[0:3])
        soup = bs(urlopen(url))
        #
        for arti, art in enumerate(soup.findAll("article", class_="u-full-height")):
            # art = soup.findAll("article", class_="u-full-height")[0]
            #
            for card in art.findAll("div", class_="c-card__body"):
                # card = soup.findAll("div", class_="c-card__body")[0]
                #
                item_title = card.h3.a.get_text()
                item_href = ''.join([url_base, card.h3.a.get_attribute_list("href")[0]])
                item_doi = 'doi.org/' + item_href.split('/')[-1]
                item_summary = card.div.p.get_text()
                #
                try:
                    authl = []
                    for authb in card.ul.findAll("li"):
                        authl.append(authb.get_text())
                    item_auth = '\n                '.join(['''<dc:creator>%s</dc:creator>''' % auth for auth in authl])
                except:
                    item_auth = ''
            #
            for data in art.findAll("div", class_="c-card__section"):
                # data = art.findAll("div", class_="c-card__section")[0]
                #
                temps = data.time.get_attribute_list("datetime")[0]
                orderx = "%s_%s" % (temps, arti)
            #
            item_list.append({'item_journal': jdic[url_sect[3]], 'item_title': item_title, 'item_summary': item_summary, 'temps': temps, 'orderx': orderx, 'item_href': item_href, 'item_doi': item_doi, 'item_author': item_auth})
    #
    #
    ## reorder by publication time
    A = [iii for iii in range(len(item_list))]
    B = [item['orderx'] for item in item_list]
    #
    idxs = [i for _,i in sorted(zip(B,A))]
    idxs.reverse()
    #
    item_list = [item_list[idx] for idx in idxs]
    #
    return(item_list)



def _usage():
    print("usage: python nature_news_views_rss.py")



#### MAIN
if __name__ == "__main__":
    main()

####



####
