import datetime
import threading
import time

from ibapi.client import EClient  # Connect between our program to IBAPI
from ibapi.wrapper import EWrapper
from ibapi.client import BarData, TagValueList, TickerId, Contract

class App(EWrapper, EClient):

    def __init__(self, host: str, port: int, conId: int) -> None:

        self.historical_bars_data: list[BarData] = []

        # Initial Eclient
        EClient.__init__(self, self)

        # Made connection
        self.connect(host, port, conId)
        
        self.event = threading.Event()

        # Start the connection socket
        con_thread = threading.Thread(target=self.run, daemon=True)
        con_thread.start()
        time.sleep(1)
    
    def historicalData(self, reqId: int, bar: BarData):
        self.historical_bars_data.append(bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        self.event.set()

app = App("127.0.0.1", 7497, 1)

def create_contract(symbol: str, sec_type: str = "STK", exchange: str = "SMART", primaryExchange: str = "ISLAND", currency: str = "USD"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exchange  # Give us the best price
    contract.primaryExchange = primaryExchange  # avoid 162 ambiguity error
    contract.currency = currency
    return contract

def get_historical_data(reqId: TickerId, contract: Contract, endDateTime: str, durationStr: str, barSizeSetting: str, whatToShow: str, useRTH: int, formatDate: int, keepUpToDate: bool, chartOptions: TagValueList):
    app.reqHistoricalData(reqId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions)
    app.event.wait()
