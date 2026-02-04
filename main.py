from scraper.scraper import Scraper
import os

def main():
    print("=== Booking.com Multi-City Hotel Scraper ===\n")

    # ---------------- User Input ----------------
    checkin = input("Enter check-in date (YYYY-MM-DD): ").strip()
    checkout = input("Enter check-out date (YYYY-MM-DD): ").strip()
    pages_input = input("Enter number of pages per city (default 3): ").strip()
    
    pages = int(pages_input) if pages_input.isdigit() else 3

    # ---------------- Top 5 Cities ----------------
    cities = ["Dubai", "Paris", "London", "New York", "Istanbul"]
    print("\nCities selected:")
    for city in cities:
        print(f"- {city}")
    
    print("\n" + "="*30)

    # ---------------- Scrape Each City ----------------
    for city in cities:
        print(f"Starting scrape for: {city}")
        print("="*30)
        scraper = Scraper(city=city, checkin=checkin, checkout=checkout, pages=pages)
        scraper.run()
        scraper.save_to_csv()
        print("\n")

    print("✅ All cities scraped successfully!")

if __name__ == "__main__":
    main()
