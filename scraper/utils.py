import csv
import os
import re


class CsvWriter:

    @staticmethod
    def save(city, rows):

        safe = re.sub(r'[\\/:*?"<>|]', "", city)

        os.makedirs("output", exist_ok=True)

        path = f"output/{safe}.csv"

        with open(path, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)
            writer.writerow(["Hotel", "Location", "Price", "Rating"])
            writer.writerows(rows)

        print(f"Saved {len(rows)} → {path}") 