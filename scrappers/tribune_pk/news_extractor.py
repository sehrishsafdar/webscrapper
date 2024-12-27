import os
import re
import requests
from bs4 import BeautifulSoup

def extract_one_page(content, url=None):
    articles = []
    soup = BeautifulSoup(content, "html.parser")
    parent_divs = soup.find_all('div', class_='col-md-12 mobile-respon phone-tech-story-sect')

    for parent_div in parent_divs:  
        article_items = parent_div.find_all('li')
        for item in article_items:
            # Extract the title
            title_element = item.find('h2', class_='title-heading add-mrgn-top lh-mb')
            title = title_element.text.strip() if title_element else None
            # Extract the link
            link_tag = item.find('div', class_='horiz-news3-caption d-flex flex-wrap')
            link_element = link_tag.find('a', href=True)
            link = link_element['href'] if link_tag else None

            articles.append({
                "Title": title,
                "Post URL": link,
            })

    return articles


url = "https://tribune.com.pk/fact-check?page=1"

response = requests.get(url)
if response.status_code == 200:
    content = response.text
    #print(content)
    articles = extract_one_page(content, url)
    print(articles)
else:
    print(f"Failed to retrieve the page: {response.status_code}")