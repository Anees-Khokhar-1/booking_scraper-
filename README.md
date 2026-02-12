# Booking.com Hotel Scraper (Python + Selenium)

A Python-based hotel scraper for Booking.com using Selenium and BeautifulSoup.

This project:

✅ Automatically finds top cities for a given country  
✅ Scrapes hotel name, location, price, and rating  
✅ Saves results into CSV files  
✅ Creates one CSV per city  
✅ Handles scrolling and dynamic loading  

---
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