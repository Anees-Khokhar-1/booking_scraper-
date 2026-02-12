from scraper.scraper import BookingScraper


def main():

    print("=== Booking.com Auto Scroll Scraper ===\n")

    country = input("Enter country or city: ").strip()
    checkin = input("Enter check-in date (YYYY-MM-DD): ").strip()
    checkout = input("Enter checkout date (YYYY-MM-DD): ").strip()

    scraper = BookingScraper(
        country=country,
        checkin=checkin,
        checkout=checkout
    )

    scraper.run()

    print("\nDONE. All hotels scraped successfully.\n")


if __name__ == "__main__":
    main()