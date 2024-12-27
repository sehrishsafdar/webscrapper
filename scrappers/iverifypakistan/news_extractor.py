import os
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def extract_one_page(content, url=None):
    articles = []
    soup = BeautifulSoup(content, "html.parser")
    parent_divs = soup.find_all('div', class_='premium-blog-wrap premium-blog-even')
    target_classes = {"false", "misleading", "true", "unproven"}

    for parent_div in parent_divs: # Loop through all parent divs
        child_divs = parent_div.find_all('div', class_=lambda value: value and value.startswith("premium-blog-post-outer-container"))
        for div in child_divs: # Loop through all child divs
            #Label
            classes = div.get('class', [])
            label = next((cls for cls in classes if cls in target_classes), None) 
            #Title
            title_tag = div.find('h2', class_='premium-blog-entry-title')
            title = title_tag.get_text(strip=True) if title_tag else None
            #URL
            link_tag = title_tag.find('a') if title_tag else None
            url = link_tag['href'] if link_tag else None
            #Date
            date_div = div.find('div', class_='premium-blog-post-time premium-blog-meta-data')
            span_tag = date_div.find('span')
            date = " ".join(span_tag.get_text(strip=True).split("|")[1:]).strip() if span_tag else None

              
            articles.append({
                "Title": title,
                "Post URL": url,
                "Date": date,
                "Label": label,
            })
    
    return articles

'''
# Initialize fake user-agent generator
ua = UserAgent()
url = "https://pak.i-verify.org/page/2/"
headers = {
    'User-Agent': ua.random  
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    content = response.text
    #print(content)
    articles = extract_one_page(content, url)
    print(articles)
else:
    print(f"Failed to retrieve the page: {response.status_code}")
'''