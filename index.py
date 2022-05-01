from utilities.App import App
from utilities.IBHelpers import IBHelpers

app = App()

app.connect("127.0.0.1", 7497, 1)

contract = IBHelpers.create_contract("AAPL", "STK", "SMART", "ISLAND", "USD")

hist_bars = app.request_historical_bars(
    1, contract, "20190201 23:59:59", "1 D", "1 hour", "TRADES", 1, 1, False, None)

print("##########--HIST BARS--##########")
for bar in hist_bars:
    print(bar)

scanner_subscription = IBHelpers.create_scanner_subscription(
    "TOP_PERC_LOSE", "STK", "STK.US.MAJOR", 50, 10, 100)

scanner_results_sell = app.request_scanner_results(
    5, scanner_subscription, [], [])
scanner_results_buy = app.request_scanner_results(
    6, scanner_subscription, [], [])

print("##########--SCANNER SELL--##########")
for scanner in scanner_results_sell:
    print(scanner)
print("##########--SCANNER BUY--##########")
for scanner in scanner_results_buy:
    print(scanner)
