import json
import zipfile
from pathlib import Path


DATA_PATH = Path("./data")


def check_for_captcha(text):
    return "CAPTCHA" in text.upper()


def load_json_from_zip(name):
    with zipfile.ZipFile(DATA_PATH / f"{name}.zip") as z:
        with z.open(f"{name}.json") as f:
            return json.load(f)


def save_json_to_zip(data, name):
    with zipfile.ZipFile(DATA_PATH / f"{name}.zip", "w") as z:
        z.writestr(f"{name}.json", json.dumps(data, ensure_ascii=False, indent=4))
        z.testzip()
