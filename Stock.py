import YFinanceImplementation

class Stock:

    def __init__(self, stock_symbol: str):
        self.stock_symbol = stock_symbol
        self.stock_price = YFinanceImplementation.YFinanceImplementation.get_stock_value(stock_symbol)
        
    def get_price(self) -> float:
        self.stock_price = YFinanceImplementation.YFinanceImplementation.get_stock_value(self.stock_symbol)
        return self.stock_price
    
    