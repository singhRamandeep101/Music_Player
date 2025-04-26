import sqlite3

class MusicPlayerDatabase:
    def __init__(self, db_name = "data/musiclibrary.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS music (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tille TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    mp3_link TEXT NOT NULL
                    )
                """)
            conn.commit()

if __name__ == "__main__":
    db = MusicPlayerDatabase()