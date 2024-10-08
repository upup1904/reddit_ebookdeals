# read url from command line and write postable version out in
# /tmp/deal.txt
# other script, post_it.py, posts from that location

import os
import re
import sys

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox


def gecko_location():
    if os.path.isfile("c:/bin/geckodriver.exe"):
        return "c:/bin/geckodriver.exe"
    else:
        if os.path.isfile("/usr/bin/geckodriver"):
            return "/usr/bin/geckodriver"
    raise RuntimeError("Need location of geckodriver. "
                       "Edit function gecko_location")


def get_browser():
    opts = Options()
    opts.headless = True

    """Get the browser (a "driver")."""
    geckopath = gecko_location()
    service = Service(geckopath)
    browser = Firefox(service=service, options=opts)
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
        if span.text.strip().lower() in ["(author)", "(author),",
                                         "(editor)", "(editor),"
                                         "(translator)", "(translator),"]:
            got_it = span.text.strip().lower()
            break
    if got_it:
        # author name might be in previous, one above that... try three times
        author = None
        entity = span
        editor_tag = " (ed.)" if "editor" in got_it else ""
        for _ in range(0, 3):
            entity = entity.previous
            try:
                author = entity.text.strip()
                if author:
                    return(author + editor_tag)
            except Exception:
                pass
        return("Can't find author")
    else:
        return("Can't find author")


def get_soup_and_direct_link(url: str) -> tuple[BeautifulSoup, str]:
    """
    :param url:
    :return: 2-tuple, the Soup to be parsed and the url to use in page (after redirection)
    """
    b = get_browser()
    b.get(url)
    html = b.page_source
    current_url = b.current_url
    b.close()
    return BeautifulSoup(html, 'html.parser'), current_url


def save_soup(soup):
    with open("/tmp/soup.html", "wb+") as s:
        s.write(bytes(soup.__repr__(), "utf-8"))
    return


def main():
    url = sys.argv[1]
    if url == "post":  # user just wants to use the next part of the calling script
        exit(0)
    soup, final_page_url = get_soup_and_direct_link(url)
    # final_page_url is what we got redirected to
    save_soup(soup)
    title = get_az_title(soup)
    price = get_az_price_kindlePriceLable(soup)
    if price is None:
        price = get_az_price_InputDisplay(soup)
    if price is None:
        price = "Can't find price"
    author = get_az_author(soup)
    booktitle = f"{title}; {author}; (Kindle; {price})"
    bookurl = final_page_url
    print(booktitle)
    with open("/tmp/deal.txt", "w+") as deal:
        deal.truncate()
        deal.write("[deal]\n")
        deal.write(f"sale = {booktitle}|^|{bookurl}\n")


if __name__ == "__main__":
    main()
