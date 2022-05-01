
from __future__ import annotations

import time
import threading

from utilities.IBApi import IBApi
from utilities.IBDataReciver import IBDataReciver

from ibapi.client import BarData, TagValueList, TickerId, Contract

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
        self.ibapi.reqHistoricalData(reqId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions)
        self.event_thread.wait()
        return self.data_reciever.get_historical_bars()
