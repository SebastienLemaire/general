
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



def make_rss_text(item_list):
    xmlt = '''<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:prism="http://prismstandard.org/namespaces/basic/2.0/" xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns="http://purl.org/rss/1.0/" xmlns:admin="http://webns.net/mvcb/">
        <channel rdf:about="https://raw.githubusercontent.com/SebastienLemaire/general/main/nature_news_views.rss">
            <title>Nature</title>
            <description>Nature publishes peer-reviewed original research of the highest quality in all areas of cell biology with an emphasis on studies that provide insights into the molecular mechanisms underlying cellular processes. The journal&amp;rsquo;s scope is broad and ranges from cytoskeletal dynamics, membrane transport, adhesion and migration, cell division, signalling pathways, development and stem cells, to molecular and cellular mechanisms underlying cancer. Nature Cell Biology provides timely and informative coverage of cell biological advances.</description>
            <link>https://raw.githubusercontent.com/SebastienLemaire/general/main/nature_news_views.rss</link>
            <admin:generatorAgent rdf:resource="https://raw.githubusercontent.com/SebastienLemaire/general/"/>
            <admin:errorReportsTo rdf:resource="mailto:sebastien.lemaire3@numericable.fr"/>
            <dc:publisher>SebastienLemaire</dc:publisher>
            <dc:language>en</dc:language>
            <dc:rights>© 2023 Sebastien Lemaire Production. All rights reserved.</dc:rights>
            <prism:publicationName>Nature Cell Biology</prism:publicationName>
            
            
            <prism:copyright>© 2023 Sebastien Lemaire Production. All rights reserved.</prism:copyright>
            <prism:rightsAgent>sebastien.lemaire3@numericable.fr</prism:rightsAgent>
            <items>
                <rdf:Seq>
                '''
    #
    #
    for item in item_list:
        xml_item_seq = '''
                        <rdf:li rdf:resource="%s"/>
        ''' % (item['item_href'])
        #
        xmlt += xml_item_seq
    #
    #
    xmlt += '''
                </rdf:Seq>
            </items>
        </channel>
        '''
    #
    #
    for item in item_list:
        xml_item = '''
            <item rdf:about="%s">
                <title><![CDATA[%s]]></title>
                <link>%s</link>
                <content:encoded>
                    <![CDATA[<p>Nature, Published online: %s; <a href="%s">doi:%s</a></p>%s]]></content:encoded>
                <dc:title><![CDATA[%s]]></dc:title>
                <dc:creator>%s</dc:creator>
                <dc:identifier>%s</dc:identifier>
                <dc:source>Nature, Published online: %s; | doi:%s</dc:source>
                <dc:date>%s</dc:date>
                <prism:publicationName>Nature</prism:publicationName>
                <prism:doi>%s</prism:doi>
                <prism:url>%s</prism:url>
            </item>
        ''' % (item['item_href'], item['item_title'], item['item_href'], item['temps'], item['item_href'], item['item_doi'], item['item_title'], item['item_title'], item['item_author'], item['item_doi'], item['temps'], item['item_doi'], item['temps'], item['item_doi'], item['item_href'])
        #
        xmlt += xml_item
    #
    #
    xmlt +='''    
    </rdf:RDF>
    '''
    #
    return(xmlt)


def update_file(xmlt):
    os.chdir('/Users/labo/')
    #
    #
    with open('/Users/labo/general/nature_news_views.rss', 'w') as fich:
        print(xmlt, file = fich)
    #
    #
    os.system('cd /Users/labo/general/')
    os.chdir('/Users/labo/general/')
    os.system('git add nature_news_views.rss')
    os.system('git commit -m "update"')
    os.system('git push -u origin main')


def retrieve_articles(url='https://www.nature.com/nature/articles?type=news-and-views'):
    domain = url.split('/')[2]
    url_base = '/'.join(url.split('/')[0:3])
    soup = bs(urlopen(url))
    #
    item_list = []
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
            try:
                item_author = card.ul.li.get_text()
            except:
                item_author = ''
        #
        for data in art.findAll("div", class_="c-card__section"):
            # data = art.findAll("div", class_="c-card__section")[0]
            #
            temps = data.time.get_attribute_list("datetime")[0]
            orderx = "%s_%s" % (temps, arti)
        #
        item_list.append({'item_title': item_title, 'item_summary': item_summary, 'temps': temps, 'orderx': orderx, 'item_href': item_href, 'item_doi': item_doi, 'item_author': item_author})
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
