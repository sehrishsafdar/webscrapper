import os
import re
from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from utils.datetime_util import convert_to_datetime
from utils.string_util import title_to_file_name
#C:\Users\Sehrish\scrapecode\webscrapper\utils


def get_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    return None

def extract_one_page(content, url=None):
    articles = []
    soup = BeautifulSoup(content, "html.parser")
    articles = soup.find_all('div', class_='col-sm-6 col-lg-4')
    for article in articles:
    # Title
     img_tag = article.find('img', class_='card-img-top')
     title = img_tag['title'] if img_tag and 'title' in img_tag.attrs else 'N/A'



    # Post URL
    post_url_tag = article.find('a', class_='text-body')
    post_url = post_url_tag['href'] if post_url_tag and 'href' in post_url_tag.attrs else 'N/A'

    # Extract the image URL
    # Image URL
    image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'N/A'

    # Fetch and save the image
    image_label = None
    if image_url:
        retrieved_image = get_image_from_url(image_url)
        if retrieved_image:
            # Convert image to RGB
            image_rgb = retrieved_image.convert("RGB")

            # Generate a sanitized file name
            file_name = title_to_file_name(title)

                # Ensure valid file extension (e.g., .png, .jpg, or .jpeg)
            if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_name += '.png'

                save_path = os.path.join("geoimages", file_name)

                # Save the image
                try:
                    image_rgb.save(save_path)
                except ValueError as e:
                    print(f"Failed to save image at {save_path}. Error: {e}")
                else:
                # Get label from the image
                    from utils.extract_label_from_image import get_image_label  # Local import to avoid circular dependency
                    image_label = get_image_label(save_path)

        # Extract the date
        date_tag = article.find('span', class_='date')
        date = date_tag.text.strip() if date_tag else 'N/A'
        converted_date = convert_to_datetime(date)

        # Append article details
        articles.append({
            "Title": title,
            "Link": post_url,
            "Date": converted_date,
            "Label": image_label,
            "Image": image_url
        })

    return articles

def extract_details(all_pages, url=None):
    all_articles = []
    for content in all_pages:
        all_articles += extract_one_page(content, url)
    return all_articles