import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_news_links(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        listview_div = soup.find("div", id="listview")
        today_news_links = []
        
        if listview_div:
            print("This is true")
            inner_divs = listview_div.find_all("div", attrs={"data-weburl": True})
            seen_urls = set()
            
            for div in inner_divs:
                print("this is getting called")
                full_url = f"https://www.livemint.com/{div['data-weburl']}"
                if full_url not in seen_urls:
                    today_news_links.append(full_url)
                    seen_urls.add(full_url)
        
        return today_news_links
        
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []