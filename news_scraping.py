import requests
from bs4 import BeautifulSoup as soup
from urllib.parse import parse_qs
import re

# my_url = f"https://www.google.com/search?q={default_location}+covid+19+news&client=firefox-b-1-d&biw=1920&bih=950&tbm=nws&ei=my-HYLC0EoTS9AOLvaj4CQ&oq={default_location}+covid+19+news&gs_l"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

def get_url(url):
    pattern = "(https.*)(&sa)"
    return re.search(pattern,url).groups()[0]


def get_articles(location="USA"):
    my_url = f"https://www.google.com/search?q={location}+covid+19&source=lnms&tbm=nws"
    source = requests.get(my_url)
    page_soup = soup(source.text, 'html.parser')

    # Grab all news divs
    containers = page_soup.find_all("div", class_="ZINbbc luh4tb xpd O9g5cc uUPGi")

    articles = []
    for container in containers:
        articles.append(
            dict(
                # source=container.find("div", class_="XTjFC WF4CUc").text,
                source=container.find("div", class_="BNeawe UPmit AP7Wnd").text,
                description=container.find("div", class_="BNeawe s3v9rd AP7Wnd").text,
                url=get_url(container.a["href"]),
                title=container.find('div', class_="BNeawe vvjwJb AP7Wnd").text
            )
        )

    return articles
