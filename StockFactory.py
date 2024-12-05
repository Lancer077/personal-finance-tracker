"""
Factory method to get stock data
Couldn't find any other stock apis that were free and fit our use case, but this allows for future additions
"""

import YFinanceImplementation
import Stock


@staticmethod
def check_valid_stock_symbol(stock_symbol: str) -> bool:
    #check yfinance
    if YFinanceImplementation.YFinanceImplementation.check_valid_stock_symbol(stock_symbol): #if yfinance can find the stock
        return True #return true
    #if we had another api to check for stock symbols, they would go here
    return False

def get_stock(stock_symbol: str) -> Stock:
    new_stock = Stock.Stock(stock_symbol)
    return new_stock
