import requests
from bs4 import BeautifulSoup
from news_extractor import extract_one_page
from fake_useragent import UserAgent

# Initialize fake User-Agent generator
ua = UserAgent()

def load_latest_posts(page):
    url = f"https://pak.i-verify.org/page/{page}/"  
    headers = {
        'User-Agent': ua.random 
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.text
        posts = extract_one_page(content)  
        soup = BeautifulSoup(content, "html.parser")

        # Check if there is a next page
        next_page_tag = soup.find('a', class_='next page-numbers')
        next = bool(next_page_tag)
        
        return posts, next
    else:
        print(f"Failed to retrieve page {page}")
        return [], False

def scrape_all_pages():
    page = 1
    all_pages_posts = []

    while True:
        posts, next = load_latest_posts(page)
        if posts:
            all_pages_posts.extend(posts)  
        if not next:
            break  
        print(f"Page {page} extracted successfully!")
        page += 1

    print('--- Data crawled from all pages! ---')
    return all_pages_posts

'''
# Start the scraping
all_posts = scrape_all_pages()
for post in all_posts:
    print(post)
'''