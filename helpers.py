from pathlib import Path

DATA_PATH = Path("./data")

def check_for_captcha(text):
    return 'CAPTCHA' in text.upper()
