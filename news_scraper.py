import requests
from bs4 import BeautifulSoup

def get_latest_news():
    url = 'https://tw.stock.yahoo.com/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    headlines = []
    for tag in soup.select('a[href*="/news"]')[:5]:
        title = tag.text.strip()
        link = tag['href']
        if not link.startswith('http'):
            link = "https://tw.stock.yahoo.com" + link
        headlines.append({"title": title, "url": link})
    return headlines
