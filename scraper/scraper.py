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


# ---------------- Helpers ----------------

def clean(text):
    return text.replace("\n", " ").strip() if text else ""


# ---------------- Scraper ----------------

class Scraper:

    BASE_URL = "https://www.booking.com/searchresults.html"

    def __init__(self, city, checkin, checkout):

        self.city = city
        self.checkin = checkin
        self.checkout = checkout
        self.results = []

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        self.wait = WebDriverWait(self.driver, 25)

    # ---------------- Build URL ----------------

    def build_url(self):

        return (
            f"{self.BASE_URL}"
            f"?ss={self.city}"
            f"&checkin={self.checkin}"
            f"&checkout={self.checkout}"
        )

    # ---------------- Auto Scroll + Load ----------------

    def auto_scroll(self):

        last_height = 0

        while True:

            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(3)

            # click Load more if exists
            try:
                btn = self.driver.find_element(
                    By.XPATH,
                    "//button/span[contains(text(),'Load')]"
                )
                self.driver.execute_script("arguments[0].click();", btn)
                print("Clicked Load More")
                time.sleep(4)
            except:
                pass

            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            if new_height == last_height:
                print("\nReached END of results.\n")
                break

            last_height = new_height

    # ---------------- Parse Hotels ----------------

    def parse_hotels(self):

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        cards = soup.select("div[data-testid='property-card']")

        print(f"Total hotels detected: {len(cards)}")

        for h in cards:

            self.results.append([
                clean(h.select_one("div[data-testid='title']").text if h.select_one("div[data-testid='title']") else ""),
                clean(h.select_one("span[data-testid='address']").text if h.select_one("span[data-testid='address']") else ""),
                clean(h.select_one("span[data-testid='price-and-discounted-price']").text if h.select_one("span[data-testid='price-and-discounted-price']") else ""),
                clean(h.select_one("div[data-testid='review-score'] div").text if h.select_one("div[data-testid='review-score'] div") else "")
            ])

    # ---------------- RUN ----------------

    def run(self):

        print(f"\nOpening {self.city}...\n")

        self.driver.get(self.build_url())

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-testid='property-card']")
            )
        )

        self.auto_scroll()
        self.parse_hotels()
        self.driver.quit()

    # ---------------- SAVE ----------------

    def save_to_csv(self):

        os.makedirs("output", exist_ok=True)
        path = f"output/{self.city}.csv"

        with open(path, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)
            writer.writerow(["Hotel", "Location", "Price", "Rating"])
            writer.writerows(self.results)

        print(f"Saved {len(self.results)} hotels → {path}")
