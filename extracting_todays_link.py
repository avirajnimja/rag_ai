import requests
from bs4 import BeautifulSoup

# Step 1: Get the webpage content
url = "https://www.livemint.com/market/stock-market-news"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Find the div with id='listview'
listview_div = soup.find("div", id="listview")

# Step 3: If found, loop through all inner divs with data-weburl attribute
today_news_link=[]
if listview_div:
    inner_divs = listview_div.find_all("div", attrs={"data-weburl": True})
    
    for div in inner_divs:
        print(f"https://www.livemint.com/{div['data-weburl']}")
        today_news_link.append("https://www.livemint.com/{div['data-weburl']}")
else:
    print("No 'listview' div found.")
