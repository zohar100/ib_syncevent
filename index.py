from utilities.App import App
from utilities.IBHelpers import IBHelpers

app = App()

app.connect("127.0.0.1", 7497, 1)

contract = IBHelpers.create_contract("AAPL", "STK", "SMART", "ISLAND", "USD")

hist_bars = app.request_historical_bars(
    1, contract, "20190201 23:59:59", "1 D", "1 hour", "TRADES", 1, 1, False, None)

for bar in hist_bars:
    print(bar)
