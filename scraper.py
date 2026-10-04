import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for the scraper
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

# Mapping written star ratings to numbers
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

books_data = []

print("Starting scraping process...")

# Scraping first 3 pages
for page in range(1, 4):
    url = BASE_URL.format(page)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch page {page}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        # 1. Extract Title
        title = article.h3.a["title"]

        # 2. Extract Price (remove currency symbol)
        price_text = article.find("p", class_="price_color").text
        price = float(price_text.encode('ascii', 'ignore').decode('utf-8'))

        # 3. Extract Star Rating
        rating_class = article.find("p", class_="star-rating")["class"]
        rating_str = rating_class[1] if len(rating_class) > 1 else "Zero"
        rating = RATING_MAP.get(rating_str, 0)

        # 4. Extract Availability
        availability = article.find("p", class_="instock availability").text.strip()

        # Append to our list
        books_data.append({
            "Title": title,
            "Price_GBP": price,
            "Rating_Stars": rating,
            "Availability": availability
        })

    print(f"Page {page} successfully scraped.")

# Convert list to a pandas DataFrame and save to CSV
df = pd.DataFrame(books_data)
df.to_csv("books_scraped_data.csv", index=False)

print("\nScraping complete!")
print(f"Total books extracted: {len(df)}")
print(df.head())
