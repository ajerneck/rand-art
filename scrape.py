import requests
import bs4
import re

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
