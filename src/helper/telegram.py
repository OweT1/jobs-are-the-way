# Standard Library Packages
import os

# Third Party Packages
import telegram
from dotenv import load_dotenv
from loguru import logger

# Load environmental variables
load_dotenv()
DEFAULT_BOT_TOKEN = os.getenv("TELEGRAM_BOT_API")


# --- Telegram Bot Class --- #
class TeleBot:
    def __init__(self, bot_token: str = DEFAULT_BOT_TOKEN):
        self.bot_token = bot_token

    async def send_message(self, text: str, chat_id: int, thread_id: int = None):
        bot = telegram.Bot(self.bot_token)
        async with bot:
            await bot.send_message(
                text=text,
                chat_id=chat_id,
                message_thread_id=thread_id,
                parse_mode=telegram.constants.ParseMode.HTML,
                disable_notification=True,
            )
        logger.info("Bot has sent message '{}' to chat {}", text, chat_id)
