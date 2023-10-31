
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from time import sleep


def get_info_from_science_highlights(url):
    ## initiate dictionnary
    idic = {}
    #
    ## retrieve the summaries
    driver = webdriver.Firefox()
    #
    # url='https://www.science.org/doi/full/10.1126/science.adl5300?af=R'
    driver.get(url)
    sleep(3)
    #
    #
    for meta in driver.find_elements(By.TAG_NAME, 'meta'):
        if meta.get_attribute('name') == 'dc.Title':
            page_title = meta.get_attribute('content')
            idic[page_title] = {}
    #
    #
    for sec in driver.find_elements(By.TAG_NAME, 'section'):
        if sec.get_attribute('id').startswith('sec-'):
            # sec = driver.find_element(By.ID, 'sec-1')
            hhh = sec.find_element(By.TAG_NAME, 'h2')
            title = '\n'.join(hhh.text.split('\n')[1:])
            idic[page_title][title] = {}
            #
            link_to_search = True
            divs = sec.find_elements(By.TAG_NAME, 'div')
            #
            #
            for divi, div in enumerate(divs):
                if div.get_attribute('role') == 'paragraph' and (div.text.startswith('Sci') or '10.' in div.text):
                    link = divs[divi].find_element(
                        By.TAG_NAME, 'a').get_attribute('href')
                    # print(link)
                    idic[page_title][title]['link'] = link
                    #
                    summ = divs[divi - 1].text
                    # print(summ)
                    idic[page_title][title]['summary'] = summ
                    #
                    break
    #
    driver.close()
    #
    return(idic)


def write_md_from_info(idic):
    otext = ''''''
    #
    for kka in idic:
        otext += '''# **%s**


''' % (kka)
        #
        for kkb in idic[kka]:
            otext += '''## [*%s*](%s)
%s


''' % (kkb, idic[kka][kkb]['link'], idic[kka][kkb]['summary'])
    #
    return(otext)





## get the Science RSS
response = urlopen('https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science')
soup = bs(response, 'html.parser')

idic = {}
for item in soup.find_all('item'):
    dctype = item.find_all('dc:type')[0]
    # print(dctype.text)
    #
    if dctype.text == 'Research Highlights':
        rhlink = item.attrs['rdf:about']
        url = rhlink
        # print(rhlink)
        #
        ## recover data
        idic.update(get_info_from_science_highlights(url))


## build the text
otext = write_md_from_info(idic)

## write the markdown file with data
import pathlib


with open(pathlib.Path('./Science_Highlights.md'), 'w', encoding='utf-8') as fich:
    print(otext, file=fich)



####
