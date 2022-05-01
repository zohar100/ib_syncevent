import threading

from ibapi.client import EClient  # Connect between our program to IBAPI
from ibapi.wrapper import EWrapper
from ibapi.client import BarData 
from ibapi.contract import ContractDetails
from ibapi.scanner import ScanData

from utilities.IBDataReciver import IBDataReciver


class IBApi(EWrapper, EClient):

    def __init__(self, event_thread: threading.Event, data_reciever: IBDataReciver) -> None:

        self.data_reciever = data_reciever

        self.event_thread = event_thread

        # Initial Eclient
        EClient.__init__(self, self)

    def historicalData(self, reqId: int, bar: BarData) -> None:
        self.data_reciever.append_historical_bar(bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str) -> None:
        self.event_thread.set()

    def scannerData(self, reqId: int, rank: int, contractDetails: ContractDetails, distance: str, benchmark: str, projection: str, legsStr: str):
        scan_data = ScanData(
            contractDetails.contract, rank, distance, benchmark, projection, legsStr)
        self.data_reciever.append_scanner_result(scan_data)
        self.event_thread.set()

    def scannerDataEnd(self, reqId: int):
        self.event_thread.set()