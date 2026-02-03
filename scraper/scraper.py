import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------- Helper Functions ----------------
def clean_text(text):
    if text:
        return text.replace("\n", " ").strip()
    return None

def parse_price(price_text):
    if price_text:
        return price_text.replace("\n", "").strip()
    return None

# ---------------- Scraper Class ----------------
class Scraper:
    def __init__(self, base_url, pages=5):
        self.base_url = base_url
        self.pages = pages
        self.hotels_data = []

        # ---------------- Chrome Options ----------------
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")  # reduce bot detection

        # ---------------- Fix for Chrome v144 ----------------
        # Automatically downloads ChromeDriver matching your browser version
        self.driver = uc.Chrome(version_main=144, options=options)

        self.wait = WebDriverWait(self.driver, 20)

    def scrape_page(self, page_number):
        print(f"Scraping page {page_number + 1}...")
        self.driver.get(self.base_url + f"&offset={page_number * 25}")

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='property-card']")))
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        hotels = soup.select("div[data-testid='property-card']")

        for hotel in hotels:
            name = clean_text(hotel.select_one("div[data-testid='title']").get_text(strip=True) if hotel.select_one("div[data-testid='title']") else None)
            location = clean_text(hotel.select_one("span[data-testid='address']").get_text(strip=True) if hotel.select_one("span[data-testid='address']") else None)
            price = parse_price(hotel.select_one("span[data-testid='price-and-discounted-price']").get_text(strip=True) if hotel.select_one("span[data-testid='price-and-discounted-price']") else None)
            rating = clean_text(hotel.select_one("div[data-testid='review-score'] div").get_text(strip=True) if hotel.select_one("div[data-testid='review-score'] div") else None)
            reviews = clean_text(hotel.select_one("div[data-testid='review-score'] div:nth-child(2)").get_text(strip=True) if hotel.select_one("div[data-testid='review-score'] div:nth-child(2)") else None)
            room_type = clean_text(hotel.select_one("div[data-testid='room-name']").get_text(strip=True) if hotel.select_one("div[data-testid='room-name']") else None)

            self.hotels_data.append([name, location, price, rating, reviews, room_type])

        time.sleep(5)

    def scrape_all(self):
        for page in range(self.pages):
            self.scrape_page(page)
        self.driver.quit()
        return self.hotels_data

    def save_to_csv(self, output_file):
        import csv
        import os
        os.makedirs("output", exist_ok=True)
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Hotel Name","Location","Price per Night","Star Rating","Number of Reviews","Room Type"])
            writer.writerows(self.hotels_data)
        print(f"Saved {len(self.hotels_data)} records to {output_file}")
