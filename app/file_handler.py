from pathlib import Path
import fitz  # PyMuPDF
from docx import Document


def read_text(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    if ext == '.pdf':
        return _read_pdf(file_path)
    elif ext in {'.docx', '.doc'}:
        return _read_docx(file_path)
    elif ext == '.txt':
        return file_path.read_text(encoding='utf-8', errors='ignore')
    else:
        raise ValueError('Formato de archivo no soportado')

def _read_pdf(file_path: Path) -> str:
    text = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text.append(page.get_text())
    return '\n'.join(text)

def _read_docx(file_path: Path) -> str:
    document = Document(file_path)
    return '\n'.join(p.text for p in document.paragraphs)
