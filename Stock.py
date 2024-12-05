"""
Factory method to get stock data
Couldn't find any other stock apis that were free and fit our use case, but this allows for future additions
"""

import YFinanceImplementation


class Stock:

    @staticmethod
    def check_valid_stock_symbol(stock_symbol: str) -> bool:
        #check yfinance
        if YFinanceImplementation.YFinanceImplementation.check_valid_stock_symbol(stock_symbol): #if yfinance can find the stock
            return True #return true
        #if we had another api to check for stock symbols, they would go here
        return False
    
    @staticmethod
    def get_stock_price(stock_symbol: str) -> float:
        price = YFinanceImplementation.YFinanceImplementation.get_stock_value(stock_symbol) 
        if type(price) == float:
            return price
        #if type of price is not a float, then we were unable to obtain a valid stock value
        #if this was the case, then here is where we would put another api to check for a stock price
        return 0 #if we cannot find the price, we just return 0, otherwise this could lead to undefined behavior

