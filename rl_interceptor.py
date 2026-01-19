import logging
import re
from typing import Protocol


class HasSetDelay(Protocol):
    def adjust_dynamic_delay(self, penalty: float) -> None:
        ...


class RLInterceptor(logging.Handler):
    _RATELIMIT_REGEX = re.compile(r"Retrying in ([0-9]*\.?[0-9]+) seconds\.")

    def __init__(self, client: HasSetDelay) -> None:
        super().__init__()
        self._client = client

    def emit(self, record: logging.LogRecord) -> None:
        msg = record.getMessage()
        match = self._RATELIMIT_REGEX.search(msg)

        if not match:
            return

        retry_after = float(match.group(1))
        self._client.adjust_dynamic_delay(retry_after)
