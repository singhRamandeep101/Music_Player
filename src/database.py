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
                return cursor.lastrowid  # Return the ID of the inserted row
        except sqlite3.Error as e:
            print(f"Error adding music: {e}")
            return None
        
    def view_library(self, title=None):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                if title:
                    cursor.execute("SELECT * FROM music WHERE title = ?", (title,))
                else:
                    cursor.execute("SELECT * FROM music")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error viewing: {e}")
            return []

    def update_music(self, music_id, title, artist, mp3_link):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE music SET title = ?, artist = ?, mp3_link = ? WHERE id = ?", (title, artist, mp3_link, music_id))
                conn.commit()
                print("Update successful")
                return True
        except sqlite3.Error as e:
            print(f"Error updating music: {e}")
            return False

    def delete_music(self, music_id):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM music WHERE id = ?", (music_id,))
                conn.commit()
                print("Delete successful")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting music: {e}")
            return False
        
    def clear_library(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM music;")
                conn.commit()
            print("Library cleared")
            return True
        except sqlite3.Error as e:
            print(f"Error clearing library: {e}")
            return False

if __name__ == "__main__":
    db = MusicPlayerDatabase()
    db.clear_library()
    music_id = db.add_music("Judas", "Lady Gaga", "abc")  # Get the ID of the added music
    print(db.view_library("Judas"))
    
    if music_id is not None:
        db.update_music(music_id, "Bad Romance", "Lady Gaga", "xyz")  # Update using the actual ID
        print(db.view_library("Bad Romance"))
        db.delete_music(music_id)  # Delete using the actual ID
        print(db.view_library())