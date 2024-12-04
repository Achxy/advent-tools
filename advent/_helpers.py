from asyncio import get_running_loop, new_event_loop, run, set_event_loop
from typing import Any, Coroutine, TypeVar

_R = TypeVar("_R")


def get_loop():
    try:
        get_running_loop()
    except RuntimeError:
        return new_event_loop()


def as_sync(coro: Coroutine[Any, Any, _R]) -> _R:
    # Downloader has a async implementation for multi-downloads that can be made using CLI
    # However, our python interface program has a sync implementation
    return run(coro, debug=False, loop_factory=new_event_loop)
