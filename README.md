# Booking.com Hotel Scraper 🏨

A Python-based web scraper that extracts hotel information from Booking.com using Selenium and BeautifulSoup.

## 🚀 Features
- Scrapes hotel name, location, price, rating, reviews, and room type
- Supports multiple pages
- Uses undetected-chromedriver to reduce bot detection
- Saves data to CSV

## 🛠 Tech Stack
- Python
- Selenium
- BeautifulSoup
- undetected-chromedriver

## 📂 Project Structure
booking_scraper/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── scraper/
│ ├── init.py
│ └── scraper.py
│
└── output/


## ⚙️ Installation

```bash
git clone https://github.com/your-username/booking_scraper.git
cd booking_scraper
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
▶️ Usage
python main.py
Enter:

City name

Check-in date

Check-out date

Number of pages to scrape

⚠️ Disclaimer
This project is for educational purposes only.
Scraping websites may violate their terms of service.

👤 Author
Anees Munir