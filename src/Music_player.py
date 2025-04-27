import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk
import os
import pygame
import time
import random
from database import MusicPlayerDatabase
from mutagen.mp3 import MP3

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iPod Music Player")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        self.is_dark_mode = False
        self.set_theme()

        self.db = MusicPlayerDatabase()
        self.current_track_index = -1
        self.is_playing = False
        self.is_paused = False
        self.current_song_duration = 0
        self.current_song_start_time = 0
        self.paused_time = 0
        self.repeat_mode = "off"  # off, one, all
        self.shuffle = False
        self.current_playlist_id = None
        self.sleep_timer = None
        self.last_song_id = None
        self.last_song_position = 0

        pygame.mixer.init()
        self.create_gui()
        self.load_last_song()

    def set_theme(self):
        bg_color = "#1e1e1e" if self.is_dark_mode else "#f0f0f0"
        fg_color = "#ffffff" if self.is_dark_mode else "#000000"
        self.root.configure(bg=bg_color)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10), padding=3, background=bg_color, foreground=fg_color)
        style.configure('TLabel', font=('Helvetica', 12), background=bg_color, foreground=fg_color)
        style.configure('TProgressbar', thickness=10, background=fg_color)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.set_theme()

    def create_gui(self):
        self.header_label = ttk.Label(self.root, text="iPod Music Player", font=('Helvetica', 16, 'bold'))
        self.header_label.pack(pady=10)

        self.track_label = ttk.Label(self.root, text="Now Playing: None", font=('Helvetica', 14, 'bold'), wraplength=350, anchor='center')
        self.track_label.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, length=350, mode='determinate')
        self.progress.pack(pady=10)

        self.time_label = ttk.Label(self.root, text="0:00 / 0:00", font=('Helvetica', 10))
        self.time_label.pack()

        self.volume_frame = tk.Frame(self.root)
        self.volume_frame.pack(pady=5)
        ttk.Label(self.volume_frame, text="Volume:", font=('Helvetica', 10)).pack(side=tk.LEFT)
        self.volume_scale = ttk.Scale(self.volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(0.5)
        pygame.mixer.music.set_volume(0.5)
        self.volume_scale.pack(side=tk.LEFT, padx=5)

        self.playlist_frame = tk.Frame(self.root)
        self.playlist_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.playlist = tk.Listbox(self.playlist_frame, height=7, width=40, selectmode=tk.SINGLE, font=('Helvetica', 10))
        self.playlist.pack(pady=5, fill=tk.BOTH, expand=True)
        self.playlist.bind('<<ListboxSelect>>', self.on_select_song)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10, fill=tk.X)

        self.library_button = ttk.Button(self.control_frame, text="Add Music", command=self.add_music, width=10)
        self.library_button.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

        self.back_button = ttk.Button(self.control_frame, text="⏮ Back", command=self.play_previous, width=10)
        self.back_button.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        self.play_pause_button = ttk.Button(self.control_frame, text="▶ Play", command=self.toggle_play_pause, width=10)
        self.play_pause_button.grid(row=0, column=2, padx=2, pady=2, sticky="ew")

        self.next_button = ttk.Button(self.control_frame, text="⏭ Next", command=self.play_next, width=10)
        self.next_button.grid(row=0, column=3, padx=2, pady=2, sticky="ew")

        self.repeat_button = ttk.Button(self.control_frame, text="Repeat: Off", command=self.toggle_repeat, width=12)
        self.repeat_button.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

        self.shuffle_button = ttk.Button(self.control_frame, text="Shuffle: Off", command=self.toggle_shuffle, width=12)
        self.shuffle_button.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        self.theme_button = ttk.Button(self.control_frame, text="Theme", command=self.toggle_theme, width=12)
        self.theme_button.grid(row=1, column=2, padx=2, pady=2, sticky="ew")

        self.sleep_button = ttk.Button(self.control_frame, text="Sleep", command=self.set_sleep_timer, width=12)
        self.sleep_button.grid(row=1, column=3, padx=2, pady=2, sticky="ew")

        self.update_playlist()

    def update_playlist(self):
        self.playlist.delete(0, tk.END)
        songs = self.db.view_library()
        for song in songs:
            self.playlist.insert(tk.END, f"{song[1]} - {song[2]} ({song[3] or 'Unknown Album'})")

    def on_select_song(self, event):
        selection = self.playlist.curselection()
        if selection:
            self.current_track_index = selection[0]

    def add_music(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if not file_path:
            return

        title = simpledialog.askstring("Input", "Enter song title:", parent=self.root)
        artist = simpledialog.askstring("Input", "Enter artist name:", parent=self.root)
        album = simpledialog.askstring("Input", "Enter album name:", parent=self.root)
        genre = simpledialog.askstring("Input", "Enter genre:", parent=self.root)

        if title and artist and os.path.isfile(file_path):
            try:
                audio = MP3(file_path)
                duration = audio.info.length
            except Exception as e:
                print(f"Error getting duration: {e}")
                duration = 180  # Fallback

            music_id = self.db.add_music(title, artist, album, genre, duration, file_path)
            if music_id:
                messagebox.showinfo("Success", f"Added {title} by {artist} to the library.")
                self.update_playlist()
            else:
                messagebox.showerror("Error", "Failed to add music.")
        else:
            messagebox.showerror("Error", "Invalid input or file not found.")

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value))

    def play_music(self):
        if self.current_track_index < 0:
            messagebox.showwarning("Warning", "Please select a song to play.")
            return
        songs = self.db.view_library()
        if not songs:
            messagebox.showwarning("Warning", "No songs in the library.")
            return

        try:
            song = songs[self.current_track_index]
            pygame.mixer.music.load(song[6])
            pygame.mixer.music.play()
            self.track_label.config(text=f"{song[1]} by {song[2]}")
            self.is_playing = True
            self.update_progress()
        except pygame.error as e:
            messagebox.showerror("Error", f"Failed to play song: {e}")

    def toggle_play_pause(self):
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.play_pause_button.config(text="⏸ Pause")
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_pause_button.config(text="▶ Play")
        else:
            self.play_music()

    def play_previous(self):
        if self.current_track_index > 0:
            self.current_track_index -= 1
            self.play_music()

    def play_next(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.db.view_library())
        self.play_music()

    def toggle_repeat(self):
        self.repeat_mode = "one" if self.repeat_mode == "off" else "off"
        self.repeat_button.config(text=f"Repeat: {self.repeat_mode.capitalize()}")

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        self.shuffle_button.config(text=f"Shuffle: {'On' if self.shuffle else 'Off'}")

    def update_progress(self):
        # Implement progress update logic
        pass

    def set_sleep_timer(self):
        minutes = simpledialog.askinteger("Input", "Enter sleep timer minutes:", parent=self.root, minvalue=1, maxvalue=120)
        if minutes:
            if self.sleep_timer:
                self.root.after_cancel(self.sleep_timer)
            self.sleep_timer = self.root.after(minutes * 60 * 1000, self.stop_music)
            messagebox.showinfo("Success", f"Sleep timer set for {minutes} minutes.")

    def load_last_song(self):
        if self.last_song_id:
            songs = self.db.view_library()
            for i, song in enumerate(songs):
                if song[0] == self.last_song_id:
                    self.current_track_index = i
                    self.play_music()
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()