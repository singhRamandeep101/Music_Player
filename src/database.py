import sqlite3
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class MusicPlayerDatabase:
    def __init__(self, db_name=r"C:\Users\32gur\Music_Player\data\musiclibrary.db"):
        self.db_name = os.path.abspath(db_name)
        logging.info(f"Database path: {self.db_name}")
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
            logging.info("Database initialized")

    def execute_query(self, query, params=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def add_music(self, title, artist, album, genre, duration, mp3_link):
        try:
            query = "INSERT INTO music(title, artist, album, genre, duration, mp3_link) VALUES (?, ?, ?, ?, ?, ?)"
            cursor = self.execute_query(query, (title, artist, album, genre, duration, mp3_link))
            music_id = cursor.lastrowid
            logging.info(f"Added music: {title} by {artist}, ID: {music_id}")
            return music_id
        except sqlite3.Error as e:
            logging.error(f"Error adding music: {e}")
            return None

    def view_library(self, title=None):
        try:
            query = "SELECT * FROM music WHERE title LIKE ?" if title else "SELECT * FROM music"
            params = (f"%{title}%",) if title else ()
            cursor = self.execute_query(query, params)
            results = cursor.fetchall()
            logging.info(f"Library view (title={title}): {results}")
            return results
        except sqlite3.Error as e:
            logging.error(f"Error viewing library: {e}")
            return []

    def update_music(self, music_id, title, artist, album, genre, duration, mp3_link):
        try:
            query = "UPDATE music SET title = ?, artist = ?, album = ?, genre = ?, duration = ?, mp3_link = ? WHERE id = ?"
            self.execute_query(query, (title, artist, album, genre, duration, mp3_link, music_id))
            logging.info(f"Updated music ID {music_id}")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error updating music: {e}")
            return False

    def delete_music(self, music_id):
        try:
            self.execute_query("DELETE FROM music WHERE id = ?", (music_id,))
            logging.info(f"Deleted music ID {music_id}")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error deleting music: {e}")
            return False

    def clear_library(self):
        try:
            self.execute_query("DELETE FROM music")
            self.execute_query("DELETE FROM playlists")
            self.execute_query("DELETE FROM playlist_songs")
            logging.info("Library cleared")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error clearing library: {e}")
            return False

    def create_playlist(self, name):
        try:
            query = "INSERT INTO playlists(name) VALUES (?)"
            cursor = self.execute_query(query, (name,))
            playlist_id = cursor.lastrowid
            logging.info(f"Created playlist: {name}, ID: {playlist_id}")
            return playlist_id
        except sqlite3.Error as e:
            logging.error(f"Error creating playlist: {e}")
            return None

    def add_song_to_playlist(self, playlist_id, music_id):
        try:
            query = "INSERT INTO playlist_songs(playlist_id, music_id) VALUES (?, ?)"
            self.execute_query(query, (playlist_id, music_id))
            logging.info(f"Added music ID {music_id} to playlist ID {playlist_id}")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error adding song to playlist: {e}")
            return False

    def view_playlists(self):
        try:
            cursor = self.execute_query("SELECT id, name FROM playlists")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error viewing playlists: {e}")
            return []

    def view_playlist_songs(self, playlist_id):
        try:
            query = """
                SELECT m.* FROM music m
                JOIN playlist_songs ps ON m.id = ps.music_id
                WHERE ps.playlist_id = ?
            """
            cursor = self.execute_query(query, (playlist_id,))
            results = cursor.fetchall()
            logging.info(f"Playlist songs (playlist_id={playlist_id}): {results}")
            return results
        except sqlite3.Error as e:
            logging.error(f"Error viewing playlist songs: {e}")
            return []