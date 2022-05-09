
from __future__ import annotations

import time
import threading

from utilities.IBApi import IBApi
from utilities.IBDataReciver import IBDataReciver

from ibapi.client import BarData, TagValueList, TickerId, Contract
from ibapi.scanner import ScanData, ScannerSubscription
from ibapi.tag_value import TagValue

class App():
    def __init__(self) -> None:
        self.data_reciever = IBDataReciver()

        self.event_thread = threading.Event()

        self.ibapi = IBApi(self.event_thread, self.data_reciever)

        self.connection_thread = threading.Thread(
            target=self.ibapi.run, daemon=True)

    def connect(self, host: str, port: int, conId: int) -> None:
        self.ibapi.connect(host, port, conId)
        self.connection_thread.start()
        time.sleep(1)

    def request_historical_bars(self, reqId: TickerId, contract: Contract, endDateTime: str, durationStr: str, barSizeSetting: str, whatToShow: str, useRTH: int, formatDate: int, keepUpToDate: bool, chartOptions: TagValueList) -> list[BarData] or None:
        self.event_thread.clear()
        self.ibapi.reqHistoricalData(reqId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions)
        self.event_thread.wait()

        results = self.data_reciever.get_historical_bars()
        self.data_reciever.clear_historical_bars()
        return results
    
    def request_scanner_results(self, reqId: TickerId, subscription: ScannerSubscription, scannerSubscriptionOptions: list[TagValue], scannerSubscriptionFilterOptions: list[TagValue]) -> list[ScanData] or None:
        self.event_thread.clear()
        self.ibapi.reqScannerSubscription(reqId, subscription, scannerSubscriptionOptions, scannerSubscriptionFilterOptions)
        self.event_thread.wait()

        self.event_thread.clear()
        self.ibapi.cancelScannerSubscription(reqId)
        self.event_thread.wait()

        results = self.data_reciever.get_scanner_results()
        self.data_reciever.clear_scanner_results()
        return results
    
    def request_account_summary(self, reqId: TickerId, groupName: str, tags: str):
        self.event_thread.clear()
        self.ibapi.reqAccountSummary(reqId, groupName, tags)
        self.event_thread.wait()
        
        self.event_thread.clear()
        self.ibapi.cancelAccountSummary(reqId)
        self.event_thread.wait()

        results = self.data_reciever.get_account_summary_tags()
        self.data_reciever.clear_account_summary_tags()
        return results