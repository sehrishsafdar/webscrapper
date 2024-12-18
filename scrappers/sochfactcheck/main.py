import csv
from scrappers.sochfactcheck.news_extractor import extract_details
from scrappers.sochfactcheck.crawl_all_news import scrape_all_pages
from datetime import datetime
from utils import string_util
all_pages = scrape_all_pages()
all_articles = []


all_articles = extract_details(all_pages)

print('--- Data extracted from all pages! ---')

# Sort articles by the 'Date' key
sorted_articles = sorted(
    all_articles,
    key=lambda x: x["Date"]
)

with open("soch_factcheck_articles.csv", "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames=["Title", "Link", "posturl", "Date", "Claim", "Label", "Image"])
    writer.writeheader() 
    writer.writerows(sorted_articles)