from pathlib import Path
from typing import List
from pydub import AudioSegment
import pygame

pygame.mixer.init()


def merge_audios(audio_paths: List[Path], output_path: Path) -> Path:
    combined = AudioSegment.empty()
    for path in audio_paths:
        combined += AudioSegment.from_file(path)
    combined.export(output_path, format='mp3')
    return output_path


def play_audio(file_path: Path):
    pygame.mixer.music.load(str(file_path))
    pygame.mixer.music.play()


def stop_audio():
    pygame.mixer.music.stop()
