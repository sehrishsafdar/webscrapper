import csv
from crawl_all_news import scrape_all_pages
from datetime import datetime

# Scrape all pages
all_pages = scrape_all_pages()

print('--- Data extracted from all pages! ---')

# Sort articles by the 'Date' key
sorted_articles = sorted(
    all_pages,
    key=lambda x: datetime.strptime(x["Date"], "%B %d, %Y"),  # Convert the Date string to a datetime object
)

with open("iverify_articles.csv", "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames=["Title", "Post URL", "Date", "Label"])
    writer.writeheader() 
    writer.writerows(sorted_articles)