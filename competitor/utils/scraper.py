import requests
from bs4 import BeautifulSoup


def scrape_price_from_url(url, selector):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        element = soup.select_one(selector)
        if element:
            text = (
                element.text.strip()
                .replace("Rs", "")
                .replace(",", "")
                .replace("PKR", "")
            )
            return float(text)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return None
