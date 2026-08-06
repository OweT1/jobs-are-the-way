# Third Party Packages
import telegram
from loguru import logger
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# Local Project
from src.errors import is_rate_limit_error


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


def create_retry_decorator_with_predicate(
    retry_predicate, max_attempts=5, initial_wait=1, max_wait=10
):
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=initial_wait, min=initial_wait, max=max_wait),
        retry=retry_predicate,
        reraise=True,
        before_sleep=_retry_state_before_sleep,
    )


# --- Retry Decorators --- #
def _is_retryable_llm_error(error):
    # Retry transient failures, but not rate-limit/quota errors (those fail
    # over to the next client via CascadingLLMClient).
    return not is_rate_limit_error(error)


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
llm_retry_decorator = create_retry_decorator_with_predicate(
    # Retry transient failures, but do NOT retry rate-limit/quota errors:
    # those fail over to the next client via CascadingLLMClient instead.
    retry_predicate=retry_if_exception(_is_retryable_llm_error),
    max_attempts=5,
    initial_wait=15,
    max_wait=45,
)
