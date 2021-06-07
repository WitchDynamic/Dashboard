import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.parse import parse_qs

# my_url = f"https://www.google.com/search?q={default_location}+covid+19+news&client=firefox-b-1-d&biw=1920&bih=950&tbm=nws&ei=my-HYLC0EoTS9AOLvaj4CQ&oq={default_location}+covid+19+news&gs_l"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
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
    containers = page_soup.findAll("div", class_="dbsr")

    articles = []
    for container in containers:
        articles.append(
            dict(
                source=container.find("div", class_="XTjFC WF4CUc").text,
                title=container.find("div", class_="JheGif jBgGLd OSrXXb").text,
                description=container.find("div", class_="Y3v8qd").text,
                url=container.a["href"],
            )
        )

    return articles
