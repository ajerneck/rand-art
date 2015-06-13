import requests
import bs4
import re
import random

URL = 'http://longform.org'

def parse_page(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text)
    posts = soup.select('div.post')
    ## filter out posts whose second class element is not empty, because those are collections or sponsored posts.
    posts = [p for p in posts if p.attrs.get('class')[1]=='']
    return [parse_post(p) for p in posts]

def parse_post(raw):
    post = {}
    post['url'] = raw.select('div.content h2 a')[0].attrs.get('href')
    post['title'] = raw.select('div.content h2')[0].text
    return post


def parse_article(post):
    try:
        page = requests.get(post['url'])
        soup = bs4.BeautifulSoup(page.text)
        article = "".join([p.text for p in soup.select('p')])
    except requests.exceptions.MissingSchema as e:
        print "error({0}): {1}".format(e.errno, e.strerror)
        print "error fetching: " + post['url']
        article = ""
    post['text'] = article
    return post

def nr_of_pages(url):
    p = requests.get(url)
    s = bs4.BeautifulSoup(p.text)
    return int(s.select('div.pagination a')[-2].text)

def scrape(url):

    n = nr_of_pages(url)
    ## generate list of all urls.
    urls = [''.join([URL, '/posts/?page=',str(i)]) for i in range(2, n)]
    ## add the first page, the url, to the list of urls.
    urls.insert(0, urls)

    ## take a random sample.
    ## urls = random.sample(urls, 4)

    ## temporary urls.
    urls = ['http://longform.org/posts/?page=153', 'http://longform.org/posts/?page=503', 'http://longform.org/posts/?page=31', 'http://longform.org/posts/?page=459']

    ## read articles
    arts = []
    for u in urls[2:3]:
        print u
        pages = parse_page(u)
        print '-------'
        for p in pages:
            print p
            a = parse_article(p)
            print len(a['text'])
            arts.append(a)

    return arts

def main():
    x = parse_page(URL)
    print [p['url'] for p in x]
    arts =  [parse_article(p) for p in x[4:7]]
    for a in arts:
        print '\n\n----' + a['url'] + '----\n\n'
        print(a['text'][0:400])
        print("\n[...]\n")
        print(a['text'][-400:])

# main()
