from pathlib import Path

DATA_PATH = Path("./data")

def check_for_captcha(dados):
    if 'CAPTCHA' in dados:
        captcha = 'captcha'   
    else:
        captcha = 'nao-captcha'
    return captcha
