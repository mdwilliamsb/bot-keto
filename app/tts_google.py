from pathlib import Path
from typing import List, Callable
from tempfile import NamedTemporaryFile

from google.cloud import texttospeech
from dotenv import load_dotenv
import os

load_dotenv()


VOICE_MAP = {
    'Femenina': texttospeech.SsmlVoiceGender.FEMALE,
    'Masculina': texttospeech.SsmlVoiceGender.MALE
}

def synthesize_chunks(chunks: List[str], voice: str, speed: float, progress_cb: Callable[[int, int], None]) -> List[Path]:
    client = texttospeech.TextToSpeechClient()
    audio_paths = []
    total = len(chunks)
    for idx, chunk in enumerate(chunks, 1):
        synthesis_input = texttospeech.SynthesisInput(text=chunk)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code="es-US",
            ssml_gender=VOICE_MAP.get(voice, texttospeech.SsmlVoiceGender.FEMALE),
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
        )
        response = client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)
        tmp_file = NamedTemporaryFile(delete=False, suffix='.mp3')
        tmp_file.write(response.audio_content)
        tmp_file.close()
        audio_paths.append(Path(tmp_file.name))
        if progress_cb:
            progress_cb(idx, total)
    return audio_paths
