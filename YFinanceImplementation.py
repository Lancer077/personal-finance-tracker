import yfinance

class YFinanceImplementation:

    def check_valid_stock_symbol(stock_symbol: str) -> bool:
        try:
            stock = yfinance.Ticker(stock_symbol)
            cur_price = stock.fast_info.get("lastPrice")
            cur_price *= 2  #Why do we do this seemingly useless operation? I'll tell you why: yfinance has different errors for when we try to get the stock price of a symbol that
            #has never existed vs one that has previously existed but no longer does. This ensures we catch both errors. Talk about a crazy edge case.
            return True
        except:
            return False
    

    def get_stock_value(stock_symbol: str) -> float:
        stock = yfinance.Ticker(stock_symbol)
        cur_price = stock.fast_info.get("lastPrice")
        return cur_price
