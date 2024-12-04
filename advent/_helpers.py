from asyncio import run
from typing import Any, Coroutine, TypeVar

_R = TypeVar("_R")


def as_sync(coro: Coroutine[Any, Any, _R]) -> _R:
    # Downloader has a async implementation for multi-downloads that can be made using CLI
    # However, our python interface program has a sync implementation
    return run(coro, debug=False)
