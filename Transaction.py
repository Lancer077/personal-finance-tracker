from datetime import date

class Transaction:

    def __init__(self, amount: float, transaction_date: date, description: str = ""):
        self._amount = amount
        self._transaction_date = transaction_date
        self._description = description
        self._category_name = ""
        self._within_last_month = self._is_within_last_month()
        self._transaction_ID = -1
    
    # return the transaction ID
    def get_transaction_id(self) -> str:
        return self._transaction_ID
    
    def set_transaction_id(self, new_ID: str) -> bool:
        if self._transaction_ID == -1:
            self._transaction_ID = new_ID
            return True
        else:
            print("Error: can only update a transaction ID once")
            return False


    # return the transaction amount
    def get_amount(self) -> float:
        return self._amount

    # set the transaction amount
    def set_amount(self, amount: float) -> None:
        self._amount = amount

    # get the date of the transaction
    def get_transaction_date(self) -> date:
        return self._transaction_date

    # set the date of the transaction
    def set_transaction_date(self, transaction_date: date) -> None:
        self._transaction_date = transaction_date
    
    def get_description(self) -> str:
        return self._description
    
    def set_description(self, description: str) -> None:
        self._description = description

    def set_category_name(self, category_name: str) -> None:
        self._category_name = category_name
    
    def get_category_name(self) -> str:
        return self._category_name

    def print_transaction(self) -> str:
        id = f"ID: {self._transaction_ID}"
        amount = f"Amount: {self._amount}"
        transaction_date = f"Date: {self._transaction_date.date()}"
        desc = f"Description: {self._description}"
        category = f"Category: {self._category_name}"
        info = f"{id}\t{amount}\t{transaction_date}\t{desc}"
        if self._category_name != "":
            info += f"\tCategory: {self._category_name}"
        return info
    
    def get_is_within_last_month(self) -> bool:
        #if it wasn't within the last month the last time we calculated it, (due to the cold, unflinching, forever forward march of time)
        #then it probably isn't with the last month now, so reason to recalculate
        if self._within_last_month == False:
            return False
        #calculate if the transaction is within the last month
        self._within_last_month = self._is_within_last_month() #update relevant variable
        return self._within_last_month  #return
    
    #checks if the transaction is within the current month and year
    def _is_within_last_month(self) -> bool:
        #get current date
        today = date.today()
        #calculate month first because it is more likely that a month has passed instead of a full year
        if self._transaction_date.month != today.month:
            return False
        if self._transaction_date.year != today.year:
            return False
        #if it is the same date and year
        return True
        