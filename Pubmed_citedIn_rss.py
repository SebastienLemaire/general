from bs4 import BeautifulSoup as bs
from datetime import datetime
from feedgen.feed import FeedGenerator


# Load the HTML file
with open('/mnt/c/Users/slemaire/Downloads/test.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
### ??? Replace loading by dowloading 
# code:
# url = 'https://pubmed.ncbi.nlm.nih.gov/?filter=years.2021-2025&sort=date&size=50&linkname=pubmed_pubmed_citedin&from_uid=17460163'
# req=Request(url)
# html_content = urlopen(req).read()


# Parse the HTML content
soup = bs(html_content, 'html.parser')

# Extract article information using the "docsum-" prefix
articles_extracted = []

for article in soup.find_all('article'):
    # Extracting title
    title_tag = article.find(attrs={"class": "docsum-title"})
    title = title_tag.get_text(strip=True) if title_tag else 'No title'

    # Extracting link
    link_tag = article.find(attrs={"class": "docsum-pmid"})
    link = link_tag.get_text(strip=True) if title_tag else 'No link'
    link = 'https://pubmed.ncbi.nlm.nih.gov/' + link + '/'

    # Extracting authors
    authors_tag = article.find(attrs={"class": "docsum-authors"})
    authors = authors_tag.get_text(strip=True) if authors_tag else 'No authors'

    # Extracting summary
    summary_tag = article.find(attrs={"class": "docsum-snippet"})
    summary = summary_tag.get_text(strip=True) if summary_tag else 'No summary'

    articles_extracted.append({
        'title': title,
        'link': link,
        'authors': authors,
        'summary': summary
    })

def generate_rss_feed_with_feedgen(articles, file_name="rss_feed.xml"):
    fg = FeedGenerator()
    fg.title('Article RSS Feed')
    fg.link(href='https://example.com')
    fg.description('RSS Feed for Articles')
    fg.language('en')

    for article in articles:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['link'])
        fe.description(f"<p>{article['summary']}</p><p><strong>Authors:</strong> {article['authors']}</p>")
        fe.pubDate(pubDate=None)

    fg.rss_file(file_name)

# Uncomment the following line to generate the RSS feed file
generate_rss_feed_with_feedgen(articles_extracted)



### ??? Record the RSS feed file on GitHub "general" repository.

####
