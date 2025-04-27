import sqlite3
import os

class MusicPlayerDatabase:
    def __init__(self, db_name=os.path.join(os.path.dirname(__file__), "data", "musiclibrary.db")):
        self.db_name = os.path.abspath(db_name)
        print(f"Database path: {self.db_name}")
        os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS music (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    album TEXT,
                    genre TEXT,
                    duration REAL,
                    mp3_link TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlist_songs (
                    playlist_id INTEGER,
                    music_id INTEGER,
                    FOREIGN KEY (playlist_id) REFERENCES playlists(id),
                    FOREIGN KEY (music_id) REFERENCES music(id)
                )
            """)
            conn.commit()
            print("Database initialized")

    def add_music(self, title, artist, album, genre, duration, mp3_link):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO music(title, artist, album, genre, duration, mp3_link) VALUES (?, ?, ?, ?, ?, ?)",
                    (title, artist, album, genre, duration, mp3_link)
                )
                conn.commit()
                music_id = cursor.lastrowid
                print(f"Added music: {title} by {artist}, ID: {music_id}")
                return music_id
        except sqlite3.Error as e:
            print(f"Error adding music: {e}")
            return None

    def view_library(self, title=None):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                if title:
                    cursor.execute("SELECT * FROM music WHERE title LIKE ?", (f"%{title}%",))
                else:
                    cursor.execute("SELECT * FROM music")
                results = cursor.fetchall()
                print(f"Library view (title={title}): {results}")
                return results
        except sqlite3.Error as e:
            print(f"Error viewing: {e}")
            return []

    def update_music(self, music_id, title, artist, album, genre, duration, mp3_link):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE music SET title = ?, artist = ?, album = ?, genre = ?, duration = ?, mp3_link = ? WHERE id = ?",
                    (title, artist, album, genre, duration, mp3_link, music_id)
                )
                conn.commit()
                print(f"Updated music ID {music_id}")
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
                print(f"Deleted music ID {music_id}")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting music: {e}")
            return False

    def clear_library(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM music")
                cursor.execute("DELETE FROM playlists")
                cursor.execute("DELETE FROM playlist_songs")
                conn.commit()
            print("Library cleared")
            return True
        except sqlite3.Error as e:
            print(f"Error clearing library: {e}")
            return False

    def create_playlist(self, name):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO playlists(name) VALUES (?)", (name,))
                conn.commit()
                playlist_id = cursor.lastrowid
                print(f"Created playlist: {name}, ID: {playlist_id}")
                return playlist_id
        except sqlite3.Error as e:
            print(f"Error creating playlist: {e}")
            return None

    def add_song_to_playlist(self, playlist_id, music_id):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO playlist_songs(playlist_id, music_id) VALUES (?, ?)", (playlist_id, music_id))
                conn.commit()
                print(f"Added music ID {music_id} to playlist ID {playlist_id}")
                return True
        except sqlite3.Error as e:
            print(f"Error adding song to playlist: {e}")
            return False

    def view_playlists(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM playlists")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error viewing playlists: {e}")
            return []

    def view_playlist_songs(self, playlist_id):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT m.* FROM music m
                    JOIN playlist_songs ps ON m.id = ps.music_id
                    WHERE ps.playlist_id = ?
                    """,
                    (playlist_id,)
                )
                results = cursor.fetchall()
                print(f"Playlist songs (playlist_id={playlist_id}): {results}")
                return results
        except sqlite3.Error as e:
            print(f"Error viewing playlist songs: {e}")
            return []