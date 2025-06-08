import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path('conversion_history.json')

def log_conversion(input_file: str, output_file: str):
    entry = {
        'input_file': input_file,
        'output_file': output_file,
        'timestamp': datetime.now().isoformat()
    }
    data = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    data.append(entry)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
