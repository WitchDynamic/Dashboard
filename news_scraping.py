import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.parse import parse_qs

# my_url = f"https://www.google.com/search?q={default_location}+covid+19+news&client=firefox-b-1-d&biw=1920&bih=950&tbm=nws&ei=my-HYLC0EoTS9AOLvaj4CQ&oq={default_location}+covid+19+news&gs_l"


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def get_articles(location="USA"):
    my_url = f"https://www.google.com/search?q={location}+covid+19+news&client=firefox-b-1-d&biw=1920&bih=950&tbm=nws&ei=my-HYLC0EoTS9AOLvaj4CQ&oq={location}+covid+19+news&gs_l"
    # Opening connection and grabbing the page
    req = urllib.request.Request(my_url, None, headers)
    response = urllib.request.urlopen(req)
    page_html = response.read()
    response.close()
    page_soup = soup(page_html, "html.parser")

    # Grab all news divs
    containers = page_soup.findAll("div", class_="ZINbbc xpd O9g5cc uUPGi")

    articles = []
    for container in containers:
        content_div = list(container.div.next_siblings)[1]
        articles.append(
            dict(
                source=container.h3.next_sibling.text,
                title=container.h3.text,
                description=content_div.a.next_sibling.div.div.div.span.next_sibling.next_sibling,
                url=parse_qs(content_div.a["href"])["/url?q"][0],
            )
        )

    return articles
