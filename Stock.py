"""
Factory method to get stock data
Couldn't find any other stock apis that were free and fit our use case, but this allows for future additions
"""

import YFinanceImplementation


class Stock:

    def __init__(self, stock_symbol: str):
        self._stock_symbol = stock_symbol
        self._stock_price = YFinanceImplementation.YFinanceImplementation.get_stock_value(stock_symbol)    

    def get_stock_price(self) -> float:
        self._stock_price = YFinanceImplementation.YFinanceImplementation.get_stock_value(self._stock_symbol) 
        return self._stock_price
    