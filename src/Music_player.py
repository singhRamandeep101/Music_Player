import tkinter as tk
from tkinter import messagebox, simpledialog
from database import MusicPlayerDatabase
import os
import pygame

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        self.db = MusicPlayerDatabase()

        # Create buttons
        self.play_button = tk.Button(root, text="Play", command=self.play_music)
        self.play_button.pack()

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_music)
        self.pause_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_music)
        self.stop_button.pack()

        self.add_button = tk.Button(root, text="Add Music", command=self.add_music)
        self.add_button.pack()

        self.track_label = tk.Label(root, text="Now Playing: None")
        self.track_label.pack()

        pygame.mixer.init()
        self.current_track = None

    def add_music(self):
        title = simpledialog.askstring("Input", "Enter song title:")
        artist = simpledialog.askstring("Input", "Enter artist name:")
        mp3_link = simpledialog.askstring("Input", "Enter MP3 file path:")
        
        if title and artist and mp3_link and os.path.isfile(mp3_link):
            music_id = self.db.add_music(title, artist, mp3_link)
            if music_id:
                messagebox.showinfo("Success", f"Added {title} by {artist} to the library.")
            else:
                messagebox.showerror("Error", "Failed to add music.")
        else:
            messagebox.showerror("Error", "Invalid input or file not found.")

    def play_music(self):
        if self.current_track:
            pygame.mixer.music.stop()
        music_entry = self.db.view_library()
        if music_entry:
            self.current_track = music_entry[0][3]
            pygame.mixer.music.load(self.current_track)
            pygame.mixer.music.play()
            self.track_label.config(text=f"Now Playing: {music_entry[0][1]} by {music_entry[0][2]}")

    def pause_music(self):
        pygame.mixer.music.pause()
        messagebox.showinfo("Info", "Paused music!")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.track_label.config(text="Now Playing: None")
        self.current_track = None
        messagebox.showinfo("Info", "Stopped music!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()