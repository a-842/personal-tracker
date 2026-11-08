import sqlite3
import datetime
import os 
from icecream import ic

DB_FILE_PATH = "tracker.db"

conn = sqlite3.connect(DB_FILE_PATH, 
                       check_same_thread=False,
                       detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cursor = conn.cursor()


def setup():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timeline (
            id INTEGER PRIMARY KEY,
            start DATETIME,
            end DATETIME,
            type TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lastUpdate (
            date DATE PRIMARY KEY
        )
    """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS types (
                type TEXT PRIMARY KEY,
                colour TEXT,
                category TEXT,
                importance INT
            )
        """)
    cursor.execute("SELECT * FROM lastUpdate")
    isDate = cursor.fetchone()
    if not isDate:
        cursor.execute("INSERT INTO lastUpdate(date) VALUES (?)", (datetime.date(2026, 11, 3),))
    conn.commit()

def add_type(type, colour, category, importance):
    cursor.execute("""  
        INSERT INTO types(type, colour, category, importance)
        VALUES (?, ?, ?, ?)""", (type, colour, category, importance)
    )



def get_all_activities():
    cursor.execute("SELECT start, end, type FROM timeline")
    return cursor.fetchall()

def get_date_activities(date):
    #date_str = date.isoformat()
    cursor.execute("SELECT start, end, type FROM timeline WHERE DATE(end) = ? or DATE(start) = ?", (date, date))
    data = cursor.fetchall()
    clipped_data = []
    for activity in data:
        activity_start = datetime.datetime.fromisoformat(activity[0]) if isinstance(activity[0], str) else activity[0]
        activity_end = datetime.datetime.fromisoformat(activity[1]) if isinstance(activity[1], str) else activity[1]
        
        activity_start = max(activity_start, datetime.datetime.combine(date, datetime.time.min))
        activity_end = min(activity_end, datetime.datetime.combine(date, datetime.time.max))

        clipped_data.append((activity_start, activity_end, activity[2]))

    return tuple(clipped_data)

def insert_activity(start, end, type):
    cursor.execute(
        """
        INSERT INTO timeline (start, end, type)
        SELECT ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM timeline 
            WHERE start = ? AND end = ? AND type = ?
        )
        """, 
        (start, end, type, start, end, type)
    )

def get_colour(type):
    cursor.execute("SELECT colour FROM types WHERE type = ?", (type,))
    colour = cursor.fetchone()
    
    return None if colour == None else colour[0]

def get_last_update():
    cursor.execute("SELECT date FROM lastUpdate")
    last = cursor.fetchone()
    return last[0]


def set_last_update(date_val):
    cursor.execute("UPDATE lastUpdate SET date = ?", (date_val,))
    commit()

def reset(validation="NoPleaseDont"):
    global conn
    global cursor
    if validation == "YesIWantTo":
        conn.close()
        os.remove(DB_FILE_PATH)
        conn = sqlite3.connect(DB_FILE_PATH, 
                       check_same_thread=False,
                       detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()
        setup()
        set_last_update(datetime.datetime(2026, 11, 3))
        add_type("sleeping", "#3b82f6", "rest", 1)
        add_type("running", "#ff1100", "workout", 1)
        add_type("cycling", "#ff1100", "workout", 1)
        add_type("lap_swimming", "#ff1100", "workout", 1)


        conn.commit()
        
    else:
        print("Call database.reset('YesIWantTo')")


def commit():
    conn.commit()

def close():
    conn.close()



if __name__ == "__main__":
    print("running database directly")
    setup()
    commit()
  
    print(get_date_activities(datetime.date(2026, 11, 6)))
    commit()
    close()

