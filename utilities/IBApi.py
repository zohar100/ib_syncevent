from __future__ import annotations

import threading

from ibapi.client import EClient  # Connect between our program to IBAPI
from ibapi.wrapper import EWrapper
from ibapi.client import BarData
from ibapi.contract import ContractDetails
from ibapi.scanner import ScanData
from ibapi.tag_value import TagValue

from utilities.Enums import Events
from utilities.IBDataReciver import IBDataReciver
from utilities.IBHandlers import IBHandlers


class IBApi(EWrapper, EClient):

    def __init__(self, events_thread: dict[Events, threading.Event], global_state: IBDataReciver, ib_handlers: IBHandlers) -> None:

        self.global_state = global_state

        self.ib_handlers = ib_handlers

        self.event_thread = events_thread

        self.counter = 0

        # Initial Eclient
        EClient.__init__(self, self)

    def historicalData(self, reqId: int, bar: BarData) -> None:
        if self.ib_handlers.historical_bars_handler:
            self.ib_handlers.historical_bars_handler(bar)
        else:
            self.global_state.append_historical_bar(bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str) -> None:
        self.event_thread[Events.MAIN].set()

    def scannerData(self, reqId: int, rank: int, contractDetails: ContractDetails, distance: str, benchmark: str, projection: str, legsStr: str):
        scan_data = ScanData(
            contractDetails.contract, rank, distance, benchmark, projection, legsStr)
        self.global_state.append_scanner_result(scan_data)
        self.event_thread[Events.MAIN].set()

    def scannerDataEnd(self, reqId: int):
        self.event_thread[Events.SECONDARY].set()

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        self.global_state.set_account_summary_tag(TagValue(tag, value))
        self.event_thread[Events.MAIN].set()

    def accountSummaryEnd(self, reqId: int):
        self.event_thread[Events.SECONDARY].set()
