import sqlite3
import datetime


conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()
    
print("database connected")


def setup():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timeline (
            id INTEGER PRIMARY KEY,
            start TIMESTAMP,
            end TIMESTAMP,
            type TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lastUpdate (
            time TIMESTAMP PRIMARY KEY
        )
    """)


def get_all_activities():
    cursor.execute("SELECT start, end, type FROM timeline")
    return cursor.fetchall()

def get_date_activities(date):
    cursor.execute("SELECT start, end, type FROM timeline WHERE DATE(end) = ? or DATE(start) = ?", (date, date))
    return cursor.fetchall()

def insert_activity(start, end, type):
    cursor.execute(
        "INSERT INTO timeline (start, end, type) VALUES (?, ?, ?)", (start, end, type)
    )

def get_last_update():
    cursor.execute("SELECT time FROM lastUpdate")
    last = cursor.fetchone()
    return last[0] or datetime.datetime.min


def set_last_update(datetime_val):
    cursor.execute("INSERT OR REPLACE INTO lastUpdate (time) VALUES (?) ", (datetime_val,))


def commit():
    conn.commit()

def close():
    conn.close()

if __name__ == "__main__":
    print("running database directly")
    setup()
    commit()
   # insert_activity(datetime.datetime.now(), datetime.datetime.now(), "run")
    print(get_date_activities(datetime.date(2026, 11, 7)))

    commit()
    close()
