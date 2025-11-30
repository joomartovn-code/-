import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import tkinter as tk
from tkinter import filedialog
import threading
from scipy.signal import find_peaks


class Dictaphone:
    def __init__(self, sample_rate=44100, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.audio_data = None
        self.is_recording = False

    def record(self, duration=None):
        self.is_recording = True
        print("Начата запись...")

        if duration:
            self.audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels
            )
            sd.wait()
            self.is_recording = False
        else:
            self.audio_data = []
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self.callback
            ):
                while self.is_recording:
                    sd.sleep(100)

        print("Запись завершена")

    def callback(self, indata, frames, time, status):
        self.audio_data.append(indata.copy())

    def stop(self):
        self.is_recording = False
        if isinstance(self.audio_data, list):
            self.audio_data = np.concatenate(self.audio_data, axis=0)
        print("Запись остановлена")

    def save(self, filename='output.wav'):
        if self.audio_data is not None:
            write(filename, self.sample_rate,
                  (self.audio_data * 32767).astype(np.int16))
            print(f"Файл сохранен: {filename}")
        else:
            print("Нет данных для сохранения")


    def detect_animal(self):
        if self.audio_data is None:
            return "Нет данных"

        audio = self.audio_data.flatten()

       
        fft = np.abs(np.fft.rfft(audio))
        freqs = np.fft.rfftfreq(len(audio), d=1/self.sample_rate)

       
        peaks, _ = find_peaks(fft, height=np.max(fft) * 0.3)
        peak_freqs = freqs[peaks]

        print("Пики частот:", peak_freqs[:10])

        dog_range = (300, 700)
        cat_range = (600, 1200)

        dog = np.any((peak_freqs >= dog_range[0]) & (peak_freqs <= dog_range[1]))
        cat = np.any((peak_freqs >= cat_range[0]) & (peak_freqs <= cat_range[1]))

        if dog and not cat:
            return "Собака (гав-гав)"
        elif cat and not dog:
            return "Кошка (мяу-мяу)"
        elif dog and cat:
            return "Неоднозначный звук"
        else:
            return "Неизвестный звук"


class DictaphoneApp:
    def __init__(self, master):
        self.master = master
        master.title("Диктофон + Определение звуков животных")
        master.geometry("400x300")

        self.dictaphone = Dictaphone()

        self.record_btn = tk.Button(master, text="Record", command=self.start_recording)
        self.record_btn.pack(pady=5)

        self.stop_btn = tk.Button(master, text="Stop", command=self.stop_recording)
        self.stop_btn.pack(pady=5)

        self.save_btn = tk.Button(master, text="Save", command=self.save_recording)
        self.save_btn.pack(pady=5)

        self.label = tk.Label(master, text="Результат: ---", font=("Arial", 14))
        self.label.pack(pady=20)

    def start_recording(self):
        thread = threading.Thread(target=self.dictaphone.record)
        thread.start()

    def stop_recording(self):
        self.dictaphone.stop()
        result = self.dictaphone.detect_animal()
        self.label.config(text=f"Результат: {result}")
        print(result)

    def save_recording(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")]
        )
        if filename:
            self.dictaphone.save(filename)


if __name__ == "__main__":
    root = tk.Tk()
    app = DictaphoneApp(root)
    root.mainloop()