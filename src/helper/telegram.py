# Third Party Packages
import telegram
from loguru import logger

# Local Project
from src.core.config import settings
from src.helper.retry import telegram_retry_decorator


# --- Telegram Bot Class --- #
class TeleBot:
    def __init__(self, bot_token: str = settings.telegram_bot_api):
        self.bot_token = bot_token

    @telegram_retry_decorator
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
