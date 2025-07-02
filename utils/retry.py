import asyncio
import logging
from typing import Any

from config.settings import settings


async def retry_with_backoff(
        operation,
        *args,
        max_retries: int = settings.MAX_RETRIES,
        base_delay: float = 1.0,
        **kwargs
) -> Any:
    """Execute an operation with exponential backoff retry logic"""

    last_exception = Exception("No attempts made")

    for attempt in range(max_retries):
        try:
            return await operation(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                await asyncio.sleep(delay)
            else:
                logging.error(f"All {max_retries} attempts failed. Last error: {e}")

    raise last_exception
