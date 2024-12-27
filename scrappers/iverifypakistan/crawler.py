import csv
from datetime import date, datetime
from crawl_all_news import load_latest_posts
from news_extractor import extract_one_page

# Define the path to the CSV file
CSV_FILE = "iverify_articles.csv"

def get_last_row_date():
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        if rows:
            last_row = rows[-1]  # Get the last row
            try:
                # Parse the date in 'May 27, 2024' format
                return datetime.strptime(last_row["Date"], "%B %d, %Y")
            except ValueError as e:
                print(f"Error parsing date in CSV file: {e}")
                return None
        else:
            print("CSV file is empty or has no data rows.")
            return None
# Call the function to print the last row's date
#last_date = datetime.strptime(get_last_row_date(), "%Y-%m-%d %H:%M:%S")
#last_date =  datetime(2024, 11, 29)
last_date = get_last_row_date()
if last_date is None:
    # Default to some past date if the CSV is empty or the date cannot be parsed
    last_date = datetime(12, 29, 2024)

# Load recent posts
recent_posts, _ = load_latest_posts(0)
extracted_recent_posts = extract_one_page(recent_posts)

# Prepare to append new articles
new_articles = []
for article in extracted_recent_posts:
    try:
        # Parse the article date in 'May 27, 2024' format
        article_date = datetime.strptime(article["Date"], "%B %d, %Y")
    except ValueError as e:
        print(f"Error parsing article date: {e}")
        continue

    if article_date > last_date:
        new_articles.append(article)

# Append new articles to the CSV file
if len(new_articles) == 0:
    print("No new articles to save!")
else:
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Title", "Post URL", "Date", "Label"])
        writer.writerows(new_articles)
    print("New articles appended to the CSV file.")
