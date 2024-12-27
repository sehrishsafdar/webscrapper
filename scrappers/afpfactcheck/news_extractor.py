import os
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def extract_one_page(content, url=None):
    os.makedirs("afp_images", exist_ok=True)

    articles = []
    soup = BeautifulSoup(content, "html.parser")
    article_boxes = soup.find_all('article', class_='node--type-article')
    
    for container in article_boxes:
        #titles + urls
        anchor_tag = container.find('a', href=True)
        if anchor_tag:
            title = anchor_tag.get_text(strip=True)  
            link = anchor_tag['href']  
        else:
            title = 'No title found'
            link = None
        #date
        date_tag = container.find('div', class_='date-short-format')
        if date_tag and 'data-original-date' in date_tag.attrs:
            date = date_tag['data-original-date']
        #image url and extraction
        image_url = container.find('img', class_='img-fluid').get('src', None)
        # Convert relative image URL to absolute URL
        if image_url and not image_url.startswith('http'):
            base_url = url.rstrip('/')
            image_url = f"{base_url}/{image_url.lstrip('/')}"

        print(f"Attempting to download image: {image_url}")

        if image_url:
            try:
                ua = UserAgent()
                headers = {
                    'User-Agent': ua.random
                }
                response = requests.get(image_url, headers=headers)
                if response.status_code == 200:
                    # Generate a unique file name based on the title
                    sanitized_title = title.replace(" ", "_").replace("/", "_").replace("\\", "_")
                    file_name = os.path.join("afp_images", f"{sanitized_title}.jpg")
                    
                    # Save the image
                    with open(file_name, "wb") as image_file:
                        for chunk in response.iter_content(1024):
                            image_file.write(chunk)
                    print(f"Image saved: {file_name}")
                else:
                    print(f"Failed to download image: {image_url}")
            except Exception as e:
                print(f"Error downloading image: {image_url}. Error: {e}")

        

        articles.append({
            "Title": title,
            "Link": link,
            "Date": date,
            "Image": image_url
        })
    
    return articles

#Fake agent to access blocked websites
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

url = "https://factcheck.afp.com/"
response = requests.get(url,  headers=headers)
if response.status_code == 200:
    content = response.text
    #print(content)
    articles = extract_one_page(content, url)
    print(articles)
else:
    print(f"Failed to retrieve the page: {response.status_code}")

