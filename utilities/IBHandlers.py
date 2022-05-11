from typing import Callable


class IBHandlers():
    def __init__(self):
        self.historical_bars_handler: Callable or None = None
