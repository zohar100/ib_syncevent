
from ibapi.client import Contract

class IBHelpers():#
    def create_contract(symbol: str, sec_type: str, exchange: str, primaryExchange: str, currency: str):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.exchange = exchange  # Give us the best price
        contract.primaryExchange = primaryExchange  # avoid 162 ambiguity error
        contract.currency = currency
        return contract
