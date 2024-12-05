import yfinance

class YFinanceImplementation:

    @staticmethod
    def check_valid_stock_symbol(stock_symbol: str) -> bool:
        try:
            stock = yfinance.Ticker(stock_symbol)
            cur_price = stock.fast_info.get("lastPrice")
            return True
        except:
            return False
    
    @staticmethod
    def get_stock_value(stock_symbol: str) -> float:
        stock = yfinance.Ticker(stock_symbol)
        cur_price = stock.fast_info.get("lastPrice")
        return cur_price
