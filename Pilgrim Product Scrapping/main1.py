from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up Selenium WebDriver
driver = webdriver.Chrome() 

#In this section we are basically appending page=(number of pages) to the url to scrape data from next pages
# Base URL and list to hold paginated URLs
BASE_URL = "https://discoverpilgrim.com/search?q=serum&type=product&page="
#Scrapping upto 5 pages (if there are any)
PAGES_TO_SCRAPE = 5 
urls = [f"{BASE_URL}{page}" for page in range(1, PAGES_TO_SCRAPE + 1)]

# Store the data in dict
data = {"Title": [], "Price": [], "Rating": [], "Review": [], "Label": []}

# Loop through each URL
for page_number, url in enumerate(urls, start=1):
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    try:
        # Wait for the page elements to load
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item-meta__title.truncate-lines")))

        # Extract data from the current page with the matching class and store
        product_titles = driver.find_elements(By.CLASS_NAME, "product-item-meta__title.truncate-lines")
        product_prices = driver.find_elements(By.CLASS_NAME, "product-item-meta__price-list-container")
        product_ratings = driver.find_elements(By.CLASS_NAME, "reviews-rating-val")
        product_reviews = driver.find_elements(By.CLASS_NAME, "count")  # Verify class name
        product_labels = driver.find_elements(By.CLASS_NAME, "sf__pcard-tags")  # Verify class name

        # Loop through the extracted data
        for title, price, rating, review, label in zip(product_titles, product_prices, product_ratings, product_reviews, product_labels):
            data["Title"].append(title.text.strip())
            data["Price"].append(price.text.strip())
            data["Rating"].append(rating.text.strip())

            # Clean review text (removes any leading "-")
            cleaned_review = review.text.strip()
            if cleaned_review.startswith("-"):
                cleaned_review = cleaned_review[1:].strip()
            data["Review"].append(cleaned_review)
            data["Label"].append(label.text.strip())

        print(f"Scraped page {page_number} successfully.")
    except Exception as e:
        #if no data found on that page
        print(f"Failed to scrape page {page_number}: {e}")

driver.quit()

# Convert to DataFrame
df = pd.DataFrame(data)

# Use utf-8-sig for emoji compatibility
csv_filename = "products.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")  

print(f"Data has been saved to {csv_filename}")
