import Transaction
from datetime import date

class TransactionList:
    def __init__(self):
        self._income_transactions = []
        self._expense_transactions = []
        self._total_income = 0
        self._total_expenses = 0
        self._transaction_count = 0 #this is used to set transaction IDs
    
    def add_income_transaction(self, income: Transaction) -> None:
        self._transaction_count += 1  #increment our transaction count
        income.set_transaction_id(self._transaction_count)
        self._income_transactions.append(income)
        self._total_income += income._amount
    
    def add_expense_transaction(self, expense: Transaction) -> None:
        self._transaction_count += 1  #increment our transaction count
        expense.set_transaction_id(self._transaction_count)
        self._expense_transactions.append(expense)
        self._total_expenses += expense._amount

    def remove_income_transaction(self, transaction_id: int) -> bool:
        for income in self._income_transactions:
            if income._transaction_ID == transaction_id:
                self._income_transactions.remove(income)
                self._total_income -= income._amount
                return True
        return False
    
    def remove_expense_transaction(self, transaction_id: int) -> bool:
        for expense in self._expense_transactions:
            if expense._transaction_ID == transaction_id:
                self._expense_transactions.remove(expense)
                self._total_expenses -= expense._amount
                return True
        return False
    
    # Finds and returns transacton by its ID from income or expense transaction
    def get_transaction(self, transaction_id) -> Transaction:
        # Add the two lengths to find which ID they're in
        transaction_id = int(transaction_id)
        for transaction in self._income_transactions + self._expense_transactions:
            if transaction._transaction_ID == transaction_id:
                return transaction
        return None
    
    def is_transaction_in_list(self, transaction_id: int, type: str) -> bool:
        if type == "income":
            for income in self._income_transactions:
                if income._transaction_ID == transaction_id:
                    return True
        if type == "expense":
            for expense in self._expense_transactions:
                if expense._transaction_ID == transaction_id:
                    return True
        return False

    # Return the total income
    def get_total_income(self) -> float:
        return self._total_income
    
    # Return the total expenses
    def get_total_expenses(self) -> float:
        return self._total_expenses
    
    def get_transaction_count(self) -> float:
        return self._transaction_count
    
    def print_expenses(self) -> str:
        expense_list = ("Expense List:\n")
        for expense in self._expense_transactions:
            expense_list += f"{expense.print_transaction()}\n"
        return expense_list
    
    def print_incomes(self) -> str:
        income_list = "Income List:\n"
        for income in self._income_transactions:
            income_list += f"{income.print_transaction()}\n"
        return income_list
    
    def print_transactions(self) -> str:
        transactions = "Transaction List: \n\n"
        transactions += TransactionList.print_incomes(self)
        transactions += f"\n{TransactionList.print_expenses(self)}"
        return transactions
        