import time
import requests

from helpers import check_for_captcha


def get(url, retries=3, wait=300):
    user_agent = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    trials = 0
    while trials < retries:
        time.sleep(wait*trials)
        html = requests.get(url, headers=user_agent, verify=False)
        html.encoding = "utf-8"
        if check_for_captcha(html.text):
            # try again
            trials += 1
            continue
        else:
            # finish loop
            break
    return html