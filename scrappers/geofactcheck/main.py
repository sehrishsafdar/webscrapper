import csv
from news_extractor import extract_details
from crawl_all_news import scrape_all_pages

all_pages_posts = scrape_all_pages()
all_articles = []

all_articles = extract_details(all_pages_posts)

print("----Extracted data from all the pages----")



#sort articles by date key
sorted_articles = sorted(
    all_articles,
    key=lambda x: x["Date"]
)

with open("geofactcheck.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Title", "Link", "Date", "Label", "Image"])
    writer.writeheader()
    writer.writerows(sorted_articles)