import sqlite3

class MusicPlayerDatabase:
    def __init__(self, db_name="data/musiclibrary.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS music (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    mp3_link TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_music(self, title, artist, mp3_link):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO music(title, artist, mp3_link) VALUES (?, ?, ?)", (title, artist, mp3_link))
            conn.commit()
            print("success")
            return True
        except sqlite3.Error as e:
            print(f"Error adding music: {e}")
            return False

if __name__ == "__main__":
    db = MusicPlayerDatabase()
    db.add_music("Judas", "Lady Gaga", "abc")