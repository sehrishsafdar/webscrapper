import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tika import parser
import csv
import os

def page_content_extractor(content, url=None):
    articles = []
    soup = BeautifulSoup(content, "html.parser")
    parent_divs = soup.find_all('div', class_='elementor-widget-wrap elementor-element-populated')

    for div in parent_divs:
        articles.append(div.get_text(strip=True))

    return articles

def save_to_file(url, content):
    filename = url.rstrip("/").split("/")[-1] + ".txt"
    filepath = os.path.join("iverify_allarticles", filename) 
    
    os.makedirs("iverify_allarticle", exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Saved article to {filepath}")



def process_csv(file_path):
    ua = UserAgent()
    #url = "https://pak.i-verify.org/alleged-statement-attributed-to-shahbaz-gill-about-us-officials-sexuality-is-fake/"
    headers = {
    'User-Agent': ua.random  
    }
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header row if it exists
        
        for row in reader:
            if len(row) < 2:  # Ensure the row has enough columns
                print(f"Skipping invalid row: {row}")
                continue

            url = row[1]  # Assuming URLs are in the second column
            print(f"Processing URL: {url}")
            
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    page_content = response.text
                    articles = page_content_extractor(page_content)
                    
                    # Combine all articles into a single text
                    full_content = "\n\n".join(articles)
                    save_to_file(url, full_content)
                else:
                    print(f"Failed to retrieve the page: {response.status_code} for URL: {url}")
            except Exception as e:
                print(f"An error occurred while processing URL {url}: {e}")


csv_file_path = "iverify_articles.csv"
process_csv(csv_file_path)