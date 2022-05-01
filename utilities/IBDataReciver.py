from __future__ import annotations

from ibapi.client import BarData

class IBDataReciver():
    def __init__(self) -> None:
        self.historical_bars: list[BarData] = []
    
    def get_historical_bars(self) -> list[BarData]:
        return self.historical_bars

    def clear_historical_bars(self) -> None:
        self.historical_bars = []
    
    def append_historical_bar(self, historical_bar: BarData) -> None:
        self.historical_bars.append(historical_bar)