import time
import csv
import os
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ---------------- Helper Functions ----------------
def clean_text(text):
    if text:
        return text.replace("\n", " ").strip()
    return ""


def parse_price(price_text):
    if price_text:
        return price_text.replace("\n", "").strip()
    return ""


# ---------------- Scraper Class ----------------
class Scraper:

    BASE_URL = "https://www.booking.com/searchresults.html"

    def __init__(self, city, checkin, checkout, pages=3):

        self.city = city
        self.checkin = checkin
        self.checkout = checkout
        self.pages = pages
        self.hotels_data = []

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        # Increase page load timeout and wait timeout
        self.driver.set_page_load_timeout(60)
        self.wait = WebDriverWait(self.driver, 40)

    # ---------------- URL Builder ----------------
    def build_url(self, page):
        offset = page * 25
        return (
            f"{self.BASE_URL}"
            f"?ss={self.city}"
            f"&checkin={self.checkin}"
            f"&checkout={self.checkout}"
            f"&offset={offset}"
        )

    # ---------------- Page Scraper ----------------
    def scrape_page(self, page):

        print(f"Scraping {self.city} | Page {page + 1}")

        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.driver.get(self.build_url(page))
                break
            except Exception as e:
                print(f"Timeout loading page {page+1} for {self.city}, retry {attempt+1}")
                if attempt == max_retries - 1:
                    print(f"Skipping page {page+1} due to repeated timeouts")
                    return

        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-testid='property-card']")
                )
            )
        except Exception:
            print(f"No hotel cards found on page {page+1} for {self.city}")
            return

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        hotels = soup.select("div[data-testid='property-card']")

        for hotel in hotels:
            name = clean_text(
                hotel.select_one("div[data-testid='title']").get_text(strip=True)
                if hotel.select_one("div[data-testid='title']") else ""
            )
            location = clean_text(
                hotel.select_one("span[data-testid='address']").get_text(strip=True)
                if hotel.select_one("span[data-testid='address']") else ""
            )
            price = parse_price(
                hotel.select_one("span[data-testid='price-and-discounted-price']").get_text(strip=True)
                if hotel.select_one("span[data-testid='price-and-discounted-price']") else ""
            )
            rating = clean_text(
                hotel.select_one("div[data-testid='review-score'] div").get_text(strip=True)
                if hotel.select_one("div[data-testid='review-score'] div") else ""
            )
            reviews = clean_text(
                hotel.select_one("div[data-testid='review-score'] div:nth-child(2)").get_text(strip=True)
                if hotel.select_one("div[data-testid='review-score'] div:nth-child(2)") else ""
            )
            room_type = clean_text(
                hotel.select_one("div[data-testid='room-name']").get_text(strip=True)
                if hotel.select_one("div[data-testid='room-name']") else ""
            )

            self.hotels_data.append([name, location, price, rating, reviews, room_type])

        time.sleep(3)  # polite delay between pages

    # ---------------- Main Runner ----------------
    def run(self):
        for page in range(self.pages):
            self.scrape_page(page)
        self.driver.quit()

    # ---------------- Save CSV ----------------
    def save_to_csv(self):
        os.makedirs("output", exist_ok=True)
        filename = f"output/booking_{self.city}_{self.checkin}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Hotel Name", "Location", "Price", "Rating", "Reviews", "Room Type"])
            writer.writerows(self.hotels_data)

        print(f"{self.city} → Saved {len(self.hotels_data)} hotels")
        return filename
