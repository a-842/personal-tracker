import sqlite3
import datetime
import os 

DB_FILE_PATH = "tracker.db"

conn = sqlite3.connect(DB_FILE_PATH, 
                       check_same_thread=False,
                       detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cursor = conn.cursor()


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
    date_str = date.isoformat()
    cursor.execute("SELECT start, end, type FROM timeline WHERE DATE(end) = ? or DATE(start) = ?", (date_str, date_str))
    data = cursor.fetchall()
    clipped_data = []
    for activity in data:
        start = max(activity[0], datetime.datetime.combine(date, datetime.time.min))
        end = min(activity[1], datetime.datetime.combine(date, datetime.time.max))
        clipped_data.append((start, end, activity[2]))

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

def get_last_update():
    cursor.execute("SELECT time FROM lastUpdate")
    last = cursor.fetchone()
    return last[0] or datetime.datetime.min


def set_last_update(datetime_val):
    cursor.execute("INSERT OR REPLACE INTO lastUpdate (time) VALUES (?) ", (datetime_val.isoformat(),))

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
        conn.commit()
        
    else:
        print("Call database.rest('YesIWantTo')")





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

