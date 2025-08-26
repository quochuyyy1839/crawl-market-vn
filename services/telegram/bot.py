import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from config.settings import TOKEN, CHAT_ID

def send_to_telegram(message, parse_mode="Markdown"):
    """
    Gửi tin nhắn đến Telegram sử dụng python-telegram-bot library
    """
    if not message or not TOKEN or not CHAT_ID:
        print("Missing message, token, or chat_id")
        return
        
    print(f"Sending message to Telegram: {message[:50]}...")
    
    # Run async function in sync context
    asyncio.run(_send_message_async(message, parse_mode))

async def _send_message_async(message, parse_mode):
    """
    Async function to send message using telegram bot
    """
    try:
        bot = Bot(token=TOKEN)
        
        # Convert parse_mode string to ParseMode enum
        telegram_parse_mode = ParseMode.MARKDOWN if parse_mode == "Markdown" else None
        
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode=telegram_parse_mode
        )
        
        print("Message sent successfully.")
        
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")
    finally:
        # Clean up bot session
        try:
            await bot.close()
        except:
            pass
