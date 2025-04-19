import requests
from bs4 import BeautifulSoup

def get_latest_news():
    url = "https://tw.stock.yahoo.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for item in soup.select("a.Fz(20px)"):
        title = item.get_text(strip=True)
        link = item.get("href")
        if title and link:
            headlines.append({"title": title, "url": link})
        if len(headlines) >= 5:
            break
    return headlines
