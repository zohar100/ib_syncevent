
from __future__ import annotations

import time
import threading

from .utilities import IBDataReciver
from .utilities import IBEvents
from .utilities import Events
from .utilities import IBApi

from ibapi.client import BarData, TagValueList, TickerId, Contract, Order
from ibapi.scanner import ScanData, ScannerSubscription
from ibapi.tag_value import TagValue


class IBSyncEvent():
    def __init__(self) -> None:
        self.global_state = IBDataReciver()

        self.ib_handlers = IBEvents()

        self.service = None

        self.events_thread = {
            Events.HISTORICAL_DATA: threading.Event(),
            Events.SCANNER_DATA: threading.Event(),
            Events.ACCOUNT_DATA: threading.Event(),
            Events.CANCEL_DATA: threading.Event(),
        }

        self.ibapi = IBApi(self.events_thread,
                           self.global_state, self.ib_handlers)

        self.connection_thread = threading.Thread(
            target=self.ibapi.run, daemon=True)

    def error(self, reqId: int, errorCode: int, errorString: str):
        if self.service:
            print(
                f"ERROR [{self.service}] [{reqId}] [{errorCode}] [{errorString}]")
            if self.service == Events.HISTORICAL_DATA:
                self.events_thread[Events.HISTORICAL_DATA].set()
        else:
            print(f"ERROR [{reqId}] [{errorCode}] [{errorString}]")

    def connect(self, host: str, port: int, conId: int) -> None:
        self.ibapi.connect(host, port, conId)
        self.connection_thread.start()
        time.sleep(1)

    def request_historical_bars(self, reqId: TickerId, contract: Contract, endDateTime: str, durationStr: str, barSizeSetting: str, whatToShow: str, useRTH: int, formatDate: int, keepUpToDate: bool, chartOptions: TagValueList) -> list[BarData] or None:
        self.service = Events.HISTORICAL_DATA

        self.events_thread[Events.HISTORICAL_DATA].clear()
        self.ibapi.reqHistoricalData(reqId, contract, endDateTime, durationStr,
                                     barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions)
        self.events_thread[Events.HISTORICAL_DATA].wait()

        if not self.ib_handlers.historical_bars_event:
            results = self.global_state.get_historical_bars()
            self.global_state.clear_historical_bars()
            return results

    def request_scanner_results(self, reqId: TickerId, subscription: ScannerSubscription, scannerSubscriptionOptions: list[TagValue], scannerSubscriptionFilterOptions: list[TagValue]) -> list[ScanData] or None:
        self.service = Events.SCANNER_DATA

        self.events_thread[Events.SCANNER_DATA].clear()
        self.ibapi.reqScannerSubscription(
            reqId, subscription, scannerSubscriptionOptions, scannerSubscriptionFilterOptions)
        self.events_thread[Events.SCANNER_DATA].wait()

        self.events_thread[Events.CANCEL_DATA].clear()
        self.ibapi.cancelScannerSubscription(reqId)
        self.events_thread[Events.CANCEL_DATA].wait()

        results = self.global_state.get_scanner_results()
        self.global_state.clear_scanner_results()
        return results

    def request_account_summary(self, reqId: TickerId, groupName: str, tags: str) -> TagValue or None:
        self.service = Events.ACCOUNT_DATA

        self.events_thread[Events.ACCOUNT_DATA].clear()
        self.ibapi.reqAccountSummary(reqId, groupName, tags)
        self.events_thread[Events.ACCOUNT_DATA].wait()

        self.events_thread[Events.CANCEL_DATA].clear()
        self.ibapi.cancelAccountSummary(reqId)
        self.events_thread[Events.CANCEL_DATA].wait()

        results = self.global_state.get_account_summary_tag()
        self.global_state.clear_account_summary_tag()
        return results

    def place_order(self, contract: Contract, order: Order or list[Order]) -> None:
        self.service = Events.ORDER_DATA

        if type(order) is not list:
            self.ibapi.placeOrder(contract, order)
            return

        for o in order:
            self.ibapi.placeOrder(contract, o)
            return
