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

    async def _send_message(self, text: str, chat_id: int, thread_id: int = None):
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

    async def send_message(self, text: str, chat_id: int, thread_id: int = None):
        return await self._send_message(text=text, chat_id=chat_id, thread_id=thread_id)

    async def send_message_with_retry(self, text: str, chat_id: int, thread_id: int = None):
        retry_decorator = create_retry_decorator(
            max_attempts=5,
            initial_wait=5,
            max_wait=30,
            exceptions=(
                telegram.error.NetworkError,
                telegram.error.RetryAfter,
                telegram.error.TimedOut,
            ),
        )

        @retry_decorator
        async def fn():
            return await self._send_message(text=text, chat_id=chat_id, thread_id=thread_id)

        return await fn()
