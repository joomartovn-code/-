import tkinter as tk
import pygame
import os

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def abs_path(file):
    return os.path.join(BASE_DIR, file)

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def create_app():
    root = tk.Tk()
    root.title("Sound Player")
    root.geometry('350x350')
    root.resizable(False, False)

    tk.Button(root, text="Таджикистан", font=("Arial", 14),
              command=lambda: play_sound(abs_path("sounds/6625-tadzhikistan.mp3"))).pack(pady=10)

    tk.Button(root, text="Аннигиляторная пушка", font=("Arial", 14),
              command=lambda: play_sound(abs_path("sounds/8126-ja-shepnu-tebe-na-ushko-annigiljatornaja-pushka.mp3"))).pack(pady=10)

    tk.Button(root, text="Бег из мультика", font=("Arial", 14),
              command=lambda: play_sound(abs_path("sounds/Звук Бег из мультика.mp3"))).pack(pady=10)

    tk.Button(root, text="Мультяшный плач", font=("Arial", 14),
              command=lambda: play_sound(abs_path("sounds/Звук Мультяшный плач ребенка.mp3"))).pack(pady=10)

    tk.Button(root, text="Lucky Lucky", font=("Arial", 14),
              command=lambda: play_sound(abs_path("sounds/lucky-lucky.mp3"))).pack(pady=10)

    root.mainloop()

create_app()
