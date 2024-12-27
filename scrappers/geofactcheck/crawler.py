import csv
from datetime import date, datetime
from crawl_all_news import load_latest_posts
from news_extractor import extract_one_page
from utils.datetime_util import convert_to_datetime

# Define the path to the CSV file
CSV_FILE = "geofactcheck.csv"

def get_last_row_date():
    # Open the CSV file in read mode
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as csvfile:
       
        reader = csv.DictReader(csvfile)
        
        rows = list(reader)

        if rows:
            last_row = rows[-1]  # Get the last row
            return last_row["Date"]
        else:
            print("CSV file is empty or has no data rows.")

# Call the function to print the last row's date
last_date = datetime.strptime(get_last_row_date(), "%Y-%m-%d %H:%M:%S")
#last_date =  datetime(2024, 11, 29)

recent_posts, _ = load_latest_posts(0)

extracted_recent_posts = extract_one_page(recent_posts)

new_articles = []

for article in extracted_recent_posts:
  
    if article["Date"] > last_date:
        new_articles.append(article)

if len(new_articles) == 0:
    print("No new articles to save!")
else:
    
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
       
        writer = csv.DictWriter(csvfile , fieldnames=["Title","Label", "Date", "Link", "Image",])
        writer.writerows(new_articles)

    print("New articles appended to the CSV file.")