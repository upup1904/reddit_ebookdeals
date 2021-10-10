# read url from command line and write postable version out in
# /tmp/deal.txt
# other script, post_it.py, posts from that location

import codecs
import os
import re
import sys


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def get_browser():
    opts = Options()
    opts.headless = True

    """Get the browser (a "driver")."""
    browser = webdriver.Firefox(options=opts, executable_path="/usr/bin/geckodriver")
    return browser


def get_az_title(soup):
    try:
        t = soup.find(id="ebooksProductTitle")
        if not t:
            t = soup.find(id="productTitle")
        if not t:
            return "Can't find title"
        title = t.contents[0].strip()
        for remove in [": A Novel", ":A novel", ": Stories",
                       " (Vintage International)", " (Books That Changed the World)",
                       " (P.S.)", " (Vintage Contemporaries)"]:
            title = title.replace(remove, "")
    except Exception:
        title = "Can't find title"
    return title

def get_az_price_kindlePriceLable(soup):
    a = soup.find(class_ = "kindlePriceLabel")
    if a is None:
        return None
    res = re.findall(r"\$[0-9\.]+", a.text)
    try:
        while(not res):
            a = a.next
            if hasattr(a, 'text'):
                res = re.findall(r"\$[0-9\.]+", a.text)
    except:
        return None
    if not res:
        return None
    return res[0]

def get_az_price_InputDisplay(soup):
    a = soup.find_all('input')
    for i in a:
        if 'name' in i.attrs and i.attrs['name'] == 'displayedPrice':
            return(i.attrs['value'])
    return None

def get_az_canonical(soup):
    x = soup.find_all("link")
    for link in x:
        if "rel" in link.attrs.keys() and "canonical" in link.attrs["rel"]:
            link_text = link['href']
            link_parts = link_text.split('/')
            # typical link looks like //https:.../.../dp/B00000
            # the part before dp often causes probems and isn't needed
            if link_parts[-2] == 'dp' and link_parts[-4] == 'www.amazon.com':
                link_text = "/".join(link_parts)
                print(f"fixed url: {link_text}")
            else:
                print(f"Nothing to fix? {link_text}")
            return(link_text)


def get_az_author(soup):
    t = soup.find(class_="authorNameLink")
    if t:
        return t.contents[0].strip()
    # if that doesn't work, some pages have a follo-the-author class, try that
    follow = soup.select('div[class*=_follow-the-author]')
    if follow:
        author_tag = follow[0]
        anchor = author_tag.find('a')
        href = anchor['href']
        author = href.split('/')[1]
        if '-' in author:
            first, last = author.split('-', maxsplit=1)
            author = ' '.join([first, last])
        return author
    # if that doesn't work, some have a (Author) marked in a span following the authors name
    spans = soup.find_all('span')
    got_it = None
    for span in spans:
        if span.text.strip().lower() == "(author)":
            got_it = span
            break
    if got_it:
        # author name might be in previous, one above that... try three times
        author = None
        entity = span
        for _ in range(0, 3):
            entity = entity.previous
            try:
                author = entity.text.strip()
                if author:
                    return(author)
            except Exception:
                pass
        return("Can't find author")
    else:
        return("Can't find author")


def get_soup(url):
    b = get_browser()
    b.get(url)
    html = b.page_source
    b.close()
    return BeautifulSoup(html, 'html.parser')


def save_soup(soup):
    with open("/tmp/soup.html", "wb+") as s:
        s.write(bytes(soup.__repr__(), "utf-8"))
    return


def main():
    url = sys.argv[1]
    if url == "post":  # user just wants to use the next part of the calling script
        exit(0)
    soup = get_soup(url)
    save_soup(soup)
    title = get_az_title(soup)
    price = get_az_price_kindlePriceLable(soup)
    if price is None:
        price = get_az_price_InputDisplay(soup)
    if price is None:
        price = "Can't find price"
    author = get_az_author(soup)
    booktitle = f"{title}; {author}; (Kindle; {price})"
    bookurl = get_az_canonical(soup)
    print(booktitle)
    with open("/tmp/deal.txt", "w+") as deal:
        deal.truncate()
        deal.write("[deal]\n")
        deal.write(f"sale = {booktitle}|^|{bookurl}\n")


if __name__ == "__main__":
    main()
