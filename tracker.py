# tracker.py
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import concurrent.futures

ua = UserAgent()

def get_product_price(url):
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")
        title = soup.find(id="productTitle").get_text(strip=True)
        price_tag = soup.find("span", class_="a-price-whole")
        price = float(price_tag.text.replace(",", "")) if price_tag else None
        return {"title": title, "price": price, "url": url}
    except:
        return {"title": "Error", "price": None, "url": url}

def get_all_prices(url_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        return list(executor.map(get_product_price, url_list))
