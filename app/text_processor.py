import re
from typing import List

MAX_CHARS = 4500


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_text(text: str, max_chars: int = MAX_CHARS) -> List[str]:
    chunks = []
    while text:
        if len(text) <= max_chars:
            chunks.append(text)
            break
        split_index = text.rfind(' ', 0, max_chars)
        if split_index == -1:
            split_index = max_chars
        chunks.append(text[:split_index])
        text = text[split_index:].lstrip()
    return chunks
