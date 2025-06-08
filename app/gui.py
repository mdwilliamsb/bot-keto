import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List

from .file_handler import read_text
from .text_processor import clean_text, split_text
from .tts_google import synthesize_chunks
from .audio_manager import merge_audios, play_audio, stop_audio
from .logger import log_conversion

UPLOAD_DIR = Path('uploads')
OUTPUT_DIR = Path('output_audios')

class SpeechifyMedicoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Speechify Médico')
        self.file_path: Path | None = None
        self.text: str = ''
        self.audio_file: Path | None = None
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill='both', expand=True)

        self.open_btn = ttk.Button(frame, text='Cargar Archivo', command=self.open_file)
        self.open_btn.grid(row=0, column=0, pady=5, sticky='w')

        ttk.Label(frame, text='Voz:').grid(row=0, column=1, sticky='e')
        self.voice_var = tk.StringVar(value='Femenina')
        voice_menu = ttk.OptionMenu(frame, self.voice_var, 'Femenina', 'Femenina', 'Masculina')
        voice_menu.grid(row=0, column=2, padx=5, sticky='w')

        ttk.Label(frame, text='Velocidad:').grid(row=0, column=3, sticky='e')
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_entry = ttk.Entry(frame, textvariable=self.speed_var, width=5)
        speed_entry.grid(row=0, column=4, sticky='w')

        self.convert_btn = ttk.Button(frame, text='Convertir a Audio', command=self.convert)
        self.convert_btn.grid(row=0, column=5, padx=5)

        self.progress = ttk.Progressbar(frame, length=200)
        self.progress.grid(row=0, column=6, padx=5)

        self.text_preview = tk.Text(frame, height=15, wrap='word')
        self.text_preview.grid(row=1, column=0, columnspan=7, pady=10, sticky='nsew')

        player_frame = ttk.Frame(frame)
        player_frame.grid(row=2, column=0, columnspan=7, pady=5)
        self.play_btn = ttk.Button(player_frame, text='Play', command=self.play_audio)
        self.play_btn.pack(side='left')
        self.stop_btn = ttk.Button(player_frame, text='Stop', command=stop_audio)
        self.stop_btn.pack(side='left', padx=5)

        ttk.Label(frame, text='Historial:').grid(row=3, column=0, sticky='w')
        self.history_list = tk.Listbox(frame, height=5)
        self.history_list.grid(row=4, column=0, columnspan=7, sticky='nsew')

        frame.columnconfigure(6, weight=1)
        frame.rowconfigure(1, weight=1)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt'), ('PDF', '*.pdf'), ('Word', '*.docx')])
        if not file_path:
            return
        self.file_path = Path(file_path)
        UPLOAD_DIR.mkdir(exist_ok=True)
        dest = UPLOAD_DIR / self.file_path.name
        dest.write_bytes(Path(file_path).read_bytes())
        try:
            text = read_text(self.file_path)
            text = clean_text(text)
            self.text = text
            preview = text[:1000]
            self.text_preview.delete('1.0', tk.END)
            self.text_preview.insert(tk.END, preview)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def update_progress(self, current: int, total: int):
        self.progress['maximum'] = total
        self.progress['value'] = current
        self.root.update_idletasks()

    def convert(self):
        if not self.text:
            messagebox.showwarning('Atención', 'Primero carga un archivo válido')
            return
        chunks = split_text(self.text)
        voice = self.voice_var.get()
        speed = self.speed_var.get()
        try:
            audio_parts = synthesize_chunks(chunks, voice, speed, self.update_progress)
            OUTPUT_DIR.mkdir(exist_ok=True)
            output_file = OUTPUT_DIR / f"{self.file_path.stem}.mp3"
            merge_audios(audio_parts, output_file)
            for part in audio_parts:
                part.unlink(missing_ok=True)
            self.audio_file = output_file
            log_conversion(str(self.file_path), str(output_file))
            self.history_list.insert(tk.END, output_file.name)
            messagebox.showinfo('Éxito', 'Conversión completada')
        except Exception as e:
            messagebox.showerror('Error', str(e))
        finally:
            self.progress['value'] = 0

    def play_audio(self):
        if self.audio_file and self.audio_file.exists():
            play_audio(self.audio_file)
        else:
            messagebox.showwarning('Atención', 'No hay audio para reproducir')

    def run(self):
        self.root.mainloop()
