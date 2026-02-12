import time
import csv
import os
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class CsvWriter:

    @staticmethod
    def save(country, rows):

        os.makedirs("output", exist_ok=True)
        path = f"output/{country}.csv"

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Hotel", "Location", "Price", "Rating"])
            writer.writerows(rows)

        print(f"\nSaved {len(rows)} hotels → {path}")


class BookingScraper:

    BASE_URL = "https://www.booking.com/searchresults.html"

    def __init__(self, country, checkin, checkout):

        self.country = country
        self.checkin = checkin
        self.checkout = checkout
        self.hotels = []

        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 25)

    # ---------- Driver ----------

    def _init_driver(self):

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    # ---------- URL ----------

    def build_url(self):

        country_encoded = quote_plus(self.country)

        return (
            f"{self.BASE_URL}"
            f"?ss={country_encoded}"
            f"&checkin={self.checkin}"
            f"&checkout={self.checkout}"
        )

    # ---------- Scroll + Load ----------

    def auto_scroll_and_scrape(self):

        last_count = 0
        same_count_hits = 0

        while True:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)

            # Click Load More if exists
            try:
                btn = self.driver.find_element(By.XPATH, "//button/span[contains(text(),'Load more')]")
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(3)
            except:
                pass

            self.scrape_hotels()

            current = len(self.hotels)

            print("Collected:", current)

            if current == last_count:
                same_count_hits += 1
            else:
                same_count_hits = 0

            if same_count_hits >= 3:
                print("\nReached END of results.")
                break

            last_count = current

    # ---------- Parsing ----------

    def scrape_hotels(self):

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        cards = soup.select("div[data-testid='property-card']")

        for card in cards:

            name = card.select_one("div[data-testid='title']")
            location = card.select_one("span[data-testid='address']")
            price = card.select_one("span[data-testid='price-and-discounted-price']")
            rating = card.select_one("div[data-testid='review-score'] div")

            row = [
                name.text.strip() if name else "",
                location.text.strip() if location else "",
                price.text.strip() if price else "",
                rating.text.strip() if rating else ""
            ]

            if row not in self.hotels:
                self.hotels.append(row)

    # ---------- Public API ----------

    def run(self):

        url = self.build_url()

        print("\nOpening:", url)

        self.driver.get(url)

        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='property-card']"))
        )

        self.auto_scroll_and_scrape()

        CsvWriter.save(self.country, self.hotels)

        self.driver.quit()

        return self.hotels