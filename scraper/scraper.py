import time
import csv
import os
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Scraper:

    BASE_URL = "https://www.booking.com/searchresults.html"

    def __init__(self, city, checkin, checkout):

        self.city = city
        self.checkin = checkin
        self.checkout = checkout
        self.hotels = []

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    # ---------------- URL ----------------

    def build_url(self):

        return (
            f"{self.BASE_URL}"
            f"?ss={self.city}"
            f"&checkin={self.checkin}"
            f"&checkout={self.checkout}"
        )

    # ---------------- AUTO LOAD EVERYTHING ----------------

    def auto_load_all(self):

        self.driver.get(self.build_url())
        time.sleep(5)

        last_height = 0

        while True:

            # Scroll bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            # Click Load More if exists
            try:
                btn = self.driver.find_element(By.XPATH, "//button/span[contains(text(),'Load more')]")
                self.driver.execute_script("arguments[0].click();", btn)
                print("Clicked Load More")
                time.sleep(4)
            except:
                pass

            # Check scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                print("\nReached END of results.\n")
                break

            last_height = new_height

    # ---------------- SCRAPE ----------------

    def scrape(self):

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        cards = soup.select("div[data-testid='property-card']")

        print(f"Total hotels detected: {len(cards)}")

        for h in cards:

            name = h.select_one("div[data-testid='title']")
            location = h.select_one("span[data-testid='address']")
            price = h.select_one("span[data-testid='price-and-discounted-price']")
            rating = h.select_one("div[data-testid='review-score'] div")

            self.hotels.append([
                name.text.strip() if name else "",
                location.text.strip() if location else "",
                price.text.strip() if price else "",
                rating.text.strip() if rating else ""
            ])

    # ---------------- RUN ----------------

    def run(self):

        self.auto_load_all()
        self.scrape()
        self.driver.quit()

    # ---------------- SAVE ----------------

    def save_to_csv(self):

        os.makedirs("output", exist_ok=True)

        path = f"output/{self.city}.csv"

        with open(path, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)
            writer.writerow(["Hotel", "Location", "Price", "Rating"])
            writer.writerows(self.hotels)

        print(f"\nSaved {len(self.hotels)} hotels → {path}") 