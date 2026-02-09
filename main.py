from scraper.scraper import Scraper


def main():

    print("=== Booking.com Auto Pagination Scraper ===\n")

    # -------- User Input --------
    city = input("Enter city: ").strip()
    checkin = input("Enter check-in (YYYY-MM-DD): ").strip()
    checkout = input("Enter checkout (YYYY-MM-DD): ").strip()

    # -------- Initialize Scraper --------
    scraper = Scraper(city, checkin, checkout)

    # -------- Run Scraper --------
    scraper.run()

    # -------- Save CSV --------
    scraper.save_to_csv()

    print("\nDONE — All data saved successfully.\n")


if __name__ == "__main__":
    main()
