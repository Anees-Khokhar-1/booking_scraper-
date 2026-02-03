from scraper.scraper import Scraper
import os

def main():
    print("=== Booking.com Hotel Scraper ===")

    # ---------------- Get user input ----------------
    city = input("Enter city name (e.g., Paris): ").strip()
    checkin = input("Enter check-in date (YYYY-MM-DD): ").strip()
    checkout = input("Enter check-out date (YYYY-MM-DD): ").strip()
    pages = input("Enter number of pages to scrape (default 5): ").strip()

    if not pages.isdigit():
        pages = 5
    else:
        pages = int(pages)

    # ---------------- Construct URL ----------------
    base_url = f"https://www.booking.com/searchresults.html?ss={city}&checkin={checkin}&checkout={checkout}"

    # ---------------- Output File ----------------
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"booking_hotels_{city}_{checkin}.csv")

    # ---------------- Initialize Scraper ----------------
    scraper = Scraper(base_url=base_url, pages=pages)

    # ---------------- Start Scraping ----------------
    print(f"\nScraping Booking.com for {city} ({checkin} to {checkout})...")
    scraper.scrape_all()

    # ---------------- Save Data ----------------
    scraper.save_to_csv(output_file)
    print(f"Scraping completed! Data saved to {output_file}")

if __name__ == "__main__":
    main()
