from scraper.scraper import Scraper


def main():

    print("\n=== Booking.com Auto Scroll Scraper ===\n")

    city = input("Enter city: ")
    checkin = input("Enter check-in: ")
    checkout = input("Enter checkout: ")

    scraper = Scraper(city, checkin, checkout)
    scraper.run()
    scraper.save_to_csv()

    print("\nDONE All Data is Save.\n")


if __name__ == "__main__":
    main()