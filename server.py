import sqlite3
import sys
from datetime import date

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from bs4 import BeautifulSoup
from faker import Faker


def save_to_db():
    URL = "https://tvschedule.today/in/tv-schedule/romedy-now"
    HEADERS: dict[str, str] = {"User-Agent": Faker().chrome()}

    conn = sqlite3.connect("names.db", check_same_thread=False)
    cur = conn.cursor()

    try:
        response = requests.get(url=URL, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        names = soup.find("section", attrs={"class": "grid gap-6 bg-primary rounded-2xl"}).find_all("h3")

        for i, j in enumerate(names):
            query = "INSERT OR IGNORE INTO movies (date, name) VALUES (?, ?);"
            cur.execute(query, (date.today(), j.text.strip()))

            print(date.today(), i + 1, "done")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the website: {e}")

    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        cur.close()
        conn.close()


scheduler = BlockingScheduler()
trigger = CronTrigger(hour=13, minute=36, second=0)

scheduler.add_job(save_to_db, trigger)

try:
    print("Starting...")
    scheduler.start()

except KeyboardInterrupt as e:
    print("Exiting...", e)
    sys.exit(0)
