from __future__ import annotations

from ibapi.client import BarData
from ibapi.scanner import ScanData

class IBDataReciver():
    def __init__(self) -> None:
        self.historical_bars: list[BarData] = []

        self.scanner_results: list[ScanData] = []
    
    def get_historical_bars(self) -> list[BarData]:
        return self.historical_bars

    def clear_historical_bars(self) -> None:
        self.historical_bars = []
    
    def append_historical_bar(self, historical_bar: BarData) -> None:
        self.historical_bars.append(historical_bar)
    
    def get_scanner_results(self) -> list[ScanData]:
        return self.scanner_results
    
    def clear_scanner_results(self) -> None:
        self.scanner_results = []
    
    def append_scanner_result(self, scanner_result: ScanData) -> None:
        self.scanner_results.append(scanner_result)