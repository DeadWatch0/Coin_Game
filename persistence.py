import json
import os

DATA_FILE = 'save_data.json'
DEFAULTS = {
    'high_score': 0,
    # future keys: 'settings': {...}, 'unlocked_skins': [], etc.
}

def load():
    if not os.path.exists(DATA_FILE):
        return DEFAULTS.copy()
    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return DEFAULTS.copy()
    # merge defaults
    out = DEFAULTS.copy()
    out.update(data)
    return out

def save(data: dict):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)