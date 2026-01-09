# Third Party Packages
import telegram
from loguru import logger

# Local Project
from src.core.config import settings
from src.utils import create_retry_decorator


# --- Telegram Bot Class --- #
class TeleBot:
    def __init__(self, bot_token: str = settings.telegram_bot_api):
        self.bot_token = bot_token

    async def send_message(self, text: str, chat_id: int, thread_id: int = None):
        retry_decorator = create_retry_decorator(
            max_attempts=7,
            initial_wait=15,
            max_wait=45,
            exceptions=(
                telegram.error.NetworkError,
                telegram.error.RetryAfter,
                telegram.error.TimedOut,
            ),
        )

        @retry_decorator
        async def _send_message(bot_token: str, text: str, chat_id: int, thread_id: int = None):
            bot = telegram.Bot(bot_token)
            async with bot:
                await bot.send_message(
                    text=text,
                    chat_id=chat_id,
                    message_thread_id=thread_id,
                    parse_mode=telegram.constants.ParseMode.HTML,
                    disable_notification=True,
                )
            logger.info("Bot has sent message '{}' to chat {}", text, chat_id)

        return await _send_message(
            bot_token=self.bot_token, text=text, chat_id=chat_id, thread_id=thread_id
        )
