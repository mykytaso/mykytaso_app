import requests

from mykytaso_app import settings


def send_telegram_message(message: str) -> None:
    url = f"https://api.telegram.org/bot{getattr(settings, 'TELEGRAM_BOT_TOKEN')}/sendMessage"

    payload = {
        "chat_id": getattr(settings, "TELEGRAM_CHAT_ID"),
        "text": message,
        "parse_mode": "HTML",
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise Exception(f"Error sending message: {response.text}")