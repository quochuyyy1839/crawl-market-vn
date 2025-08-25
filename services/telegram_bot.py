import requests
from config import TELEGRAM_URL, CHAT_ID

def send_to_telegram(message, parse_mode="Markdown"):
    """
    Gửi tin nhắn đến Telegram với Markdown support
    """
    if not message:
        return
        
    print(f"Sending message to Telegram: {message[:50]}...")
    try:
        response = requests.post(
            TELEGRAM_URL,
            data={
                'chat_id': CHAT_ID,
                'text': message,
                'parse_mode': parse_mode
            },
            timeout=15
        )
        if response.status_code != 200:
            print(f"Error sending message: {response.status_code}, {response.text}")
        else:
            print("Message sent successfully.")
    except requests.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
