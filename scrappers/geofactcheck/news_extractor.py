import os
import re
import requests
from bs4 import BeautifulSoup
from utils.datetime_util import convert_to_datetime

#url = "https://www.geo.tv/writer/geo-fact-check"

def extract_one_page(content, url=None):
    articles =[]
    soup = BeautifulSoup(content, "html.parser")
    article_boxes = soup.find_all('div', class_='col-sm-6')
    for article_box in article_boxes:
        article_title = article_box.find('div', class_='card-body')
        h6_tag = soup.find('a', class_='text-body')
        article_date = article_box.find('span', class_='date')
        #Extract
        title = article_title.text.strip() if article_title else ''
        if h6_tag:
            post_url = h6_tag.find('a')['href']
        #Extract and convert date
        date = article_date.text.strip() if article_date else 'Unknown'
        converted_date = convert_to_datetime(date)

        #Append article details
        articles({
            "Title": title,
            "posturl": post_url,
            "Date": converted_date,
        })

    return articles

def extract_details(all_pages, url=None):
    all_articles = []
    for content in all_pages:
        all_articles +=extract_one_page(content, url)
    return all_articles








'''
def extract_one_page(content, url=None):
    articles = []
    soup = BeautifulSoup(content, "html.parser")
    article_boxes = soup.find_all('div', class_='container')
    for container in article_boxes:
        article_title = container.find('div', class_='caption')
        # Extract title
        title = article_title.text.strip() if article_title else ''
        # Append article details
        articles.append({
            "Title": title,
        })
    
    return articles
url = "https://www.geo.tv/writer/geo-fact-check"
response = requests.get(url)
content = response.text
articles = extract_one_page(content, url)
print(articles)

def extract_one_page(content, url=None):
    articles = []
    soup = BeautifulSoup(content, "html.parser")
    article_boxes = soup.find_all('div', class_='article-box')

    for article_box in article_boxes:
        article_title = article_box.find('h6')
        h6_tag = soup.find('h6', class_='fs-4 my-2')
        article_link_tag = article_box.find('a', href=True)
        article_date = article_box.find(class_='article-date')
        article_claim = article_box.find(class_='article_excerpt')
        article_label_html = article_box.find('div', class_='show-label')  # HTML label element
        label_from_html = article_label_html.text.strip() if article_label_html else None

        # Initialize variables
        image_url = None
        image_label = None

        # Extract title
        title = article_title.text.strip() if article_title else ''
        if h6_tag:
         post_url = h6_tag.find('a')['href']
        # Extract featured image
        featured_div = article_box.find('div', class_='featured-image')
        if featured_div:
            img_tag = featured_div.find('img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']

                # Fetch and save the image
                retrieved_image = get_image_from_url(image_url)
                if retrieved_image:
                    # Convert image to RGB
                    image_rgb = retrieved_image.convert("RGB")

                    # Generate a sanitized file name
                    file_name = title_to_file_name(title)

                    # Ensure valid file extension (e.g., .png, .jpg, or .jpeg)
                    if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file_name += '.png'

                    save_path = os.path.join("Sochfactcheck_images", file_name)
                    

                    # Save the image
                    try:
                        image_rgb.save(save_path)
                    except ValueError as e:
                        print(f"Failed to save image at {save_path}. Error: {e}")
                    else:
                        # Get label from the image
                        from utils.extract_label_from_image import get_image_label  # Local import to avoid circular dependency
                        image_label = get_image_label(save_path)

        # Extract article link
        link = article_link_tag['href'].strip() if article_link_tag else ''
        full_link = url + link if url and link.startswith('/') else link

        # Extract claim
        claim = article_claim.text.strip() if article_claim else 'No claim available'

        # Extract and convert date
        date = article_date.text.strip() if article_date else 'Unknown'
        converted_date = convert_to_datetime(date)

        # Decide the label: prefer image-derived label if available
        label = image_label if image_label else label_from_html

        # Append article details
        articles.append({
            "Title": title,
            "Link": full_link,
            "posturl": post_url,
            "Date": converted_date,
            "Claim": claim,
            "Label": label,
            "Image": image_url
        })

    return articles

def extract_details(all_pages, url=None):
    all_articles = []
    for content in all_pages:
        all_articles += extract_one_page(content, url)
    return all_articles
'''
