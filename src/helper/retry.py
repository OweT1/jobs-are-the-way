# Third Party Packages
import telegram
from loguru import logger
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


# --- Functions --- #
def _retry_state_before_sleep(retry_state: RetryCallState):
    logger.error(
        "Retrying {}: attempt {} ended with: {}",
        retry_state.fn,
        retry_state.attempt_number,
        retry_state.outcome,
    )


def create_retry_decorator(max_attempts=3, initial_wait=1, max_wait=10, exceptions=()):
    if exceptions:
        return retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=initial_wait, min=initial_wait, max=max_wait),
            retry=retry_if_exception_type(exceptions),
            reraise=True,  # Reraise the final exception after all attempts fail
            before_sleep=_retry_state_before_sleep,
        )
    else:
        return retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=initial_wait, min=initial_wait, max=max_wait),
            reraise=True,  # Reraise the final exception after all attempts fail
            before_sleep=_retry_state_before_sleep,
        )


# --- Retry Decorators --- #
db_retry_decorator = create_retry_decorator()
job_search_retry_decorator = create_retry_decorator()
telegram_retry_decorator = create_retry_decorator(
    max_attempts=7,
    initial_wait=15,
    max_wait=45,
    exceptions=(
        telegram.error.NetworkError,
        telegram.error.RetryAfter,
        telegram.error.TimedOut,
    ),
)
llm_retry_decorator = create_retry_decorator(
    max_attempts=7,
    initial_wait=15,
    max_wait=45,
)
