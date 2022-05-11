from utilities.App import App
from utilities.IBHelpers import IBHelpers
from utilities.IBHandlers import IBHandlers

from ibapi.account_summary_tags import AccountSummaryTags

handlers = IBHandlers()

app = App(handlers)

app.connect("127.0.0.1", 7497, 1)

# contract = IBHelpers.create_contract("AAPL", "STK", "SMART", "ISLAND", "USD")


# def on_get_hist_bar(bar):
#     print(bar)


# handlers.historical_bars_handler = on_get_hist_bar

# hist_bars = app.request_historical_bars(
#     1, contract, "20190201 23:59:59", "1 D", "1 hour", "TRADES", 1, 1, False, None)

# scanner_subscription = IBHelpers.create_scanner_subscription(
#     "TOP_PERC_LOSE", "STK", "STK.US.MAJOR", 50, 10, 100)

# scanner_results_sell = app.request_scanner_results(
#     6, scanner_subscription, [], [])
# scanner_results_buy = app.request_scanner_results(
#     7, scanner_subscription, [], [])

# print("##########--SCANNER SELL--##########")
# for scanner in scanner_results_sell:
#     print(scanner)
# print("##########--SCANNER BUY--##########")
# for scanner in scanner_results_buy:
#     print(scanner)

all_tags = AccountSummaryTags.AllTags.split(",")

for tag in all_tags:
    index = all_tags.index(tag)
    account_summary_tags = app.request_account_summary(index, "All", tag)

    print(account_summary_tags)
