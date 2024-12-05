import Operations
import Transaction
from datetime import datetime
import MainUI
import Entity
import EntityPortfolio
import TransactionList
import UserAccount
import Category
import CategoryList
import Stock

class Validator():

    transaction_list = TransactionList.TransactionList()
    entity_portfolio = EntityPortfolio.EntityPortfolio()




    #-----------PRIVATE METHODS-------------------
    # use to check if a given string can be converted to integer safely
    @staticmethod
    def _validate_integer(entry: str) -> bool:
        try:
            int(entry)
            return True
        except:
            MainUI.MainUI.integer_not_given()
            return False

    #used to check if a given string can be converted to float safely
    @staticmethod
    def _validate_float(entry: str) -> bool:
        try:
            float(entry)
            return True
        except:
            MainUI.MainUI.float_not_given()
            return False

    #another private method to check if the input integer is within a valid range
    @staticmethod
    def _validate_selection_range(selection: int, low_end: int, high_end: int) -> bool:
        if selection > high_end or selection < low_end: 
            MainUI.MainUI.invalid_selection_range(low_end, high_end)
            return False
        return True

    @staticmethod
    def validate_home_screen_entry(entry: str) -> bool:
        #technically for speed this should be implemented below the validate integer
        #however this is more readable
        low_end = 0
        high_end = 9

        #if validate integer returns false
        if not Validator._validate_integer(entry):
            return False #return false
        
        selection = int(entry)  #we can now safely cast entry to int
        if not Validator._validate_selection_range(selection, low_end, high_end): #if selection range validation is false
            return False   #return false
        
        return True
        

    @staticmethod
    def validate_menu_entry(entry: str, low_end: int, high_end: int) -> bool:
        # user's entry must be an integer
        if not Validator._validate_integer(entry):
            return False
        
        selection = int(entry)
        if not Validator._validate_selection_range(selection, low_end, high_end):
            return False
        return True

    @staticmethod
    def validate_value(amount) -> bool:
        if not Validator._validate_float(amount):
            return False
        amount = float(amount)
        if amount < 0:
            print("Error: amount cannot be negative")
            return False
        return True

    @staticmethod
    def validate_transaction_date(date) -> bool:
        '''
        method to validate a transaction date
        '''
        try:
            datetime.strptime(date, '%m/%d/%y')

        except:
            print("Error: Please format date correctly.")
            return False
        
        return True

    @staticmethod
    def are_transaction_details_valid(transaction_details: list, type: str) -> bool:
        if len(transaction_details) == 3:
            Operations.create_and_add_transaction(transaction_details, type)
            return

    @staticmethod
    def validate_transaction_id(transaction_list, transaction_id: str, type):
        if not Validator._validate_integer(transaction_id): #if we do not have a valid integer
            return False                            #automatically return false
        transaction_id = int(transaction_id)
        if transaction_id < -1:
            #print("Error: smallest allowed value is -1")
            #MainUI.MainUI.wait_for_user_input()
            return False
        if transaction_id == -1:  #always allow user to back out of deleting a transaction
            return True
        #Make sure that a transaction id that exists was entered
        if TransactionList.TransactionList.is_transaction_in_list(transaction_list, transaction_id, type):
            return True
        return False


    @staticmethod
    def validate_num_owned(num_owned: str):
        if num_owned == "": #allow for the case where the user enters nothing
            return True
        
        if not Validator._validate_integer(num_owned):
            return False
        owned = int(num_owned)
        if owned < 0:
            print("Error: cannot own negative entities")
            return False
        return True

    @staticmethod
    def validate_yes_no(user_input: str):
        if user_input == "":
            return False
        if user_input[0] == "y":
            return True
        elif user_input[0] == "n":
            return True
        return False

    #used to ensure that the user did not leave the space blank
    @staticmethod
    def validate_entity_name(user_input: str):
        if user_input == "":
            MainUI.MainUI.empty_name()
            return False
        return True

    @staticmethod
    def validate_new_category_name(category_list: CategoryList, user_input: str):
        if len(user_input) == 0:
            return False
        name_list = category_list.get_category_names()
        if user_input in name_list:
            MainUI.MainUI.category_name_already_exists(user_input)
            return False
        return True

    @staticmethod
    def validate_category_name(category_list: CategoryList, user_input: str):
        if user_input == "-1":
            return True
        category = category_list.get_category(user_input)
        if category == None:
            MainUI.MainUI.category_not_found()
            return False
        return True

    @staticmethod
    def validate_stock_symbol(stock_symbol: str):
        if stock_symbol == "":
            return False
        if not Stock.Stock.check_valid_stock_symbol(stock_symbol):  #this means advfi couldn't find the corresponding stock
            MainUI.MainUI.stock_not_found(stock_symbol)
            return False
        #if we make it here, then the user input stock symbol is valid
        return True

    @staticmethod
    def validate_entity_id(entity_portfolio, type: str, entity_id: str):
        if not Validator._validate_integer(entity_id):
            return False
        entity_id = int(entity_id)
        if entity_id < -1:
            print("Error: smallest allowed value is -1")
            return False
        if entity_id == -1: #action cancelled
            return True
        #Make sure that a transaction id that exists was entered
        if type == "asset":
            return entity_portfolio.find_asset_id(entity_id)
        if type == "liability":
            return entity_portfolio.find_liability_id(entity_id)
        return False #if by some SM64 bit switching magic we find ourselves here, prevent the program from erroring out

    @staticmethod
    def validate_payment_debt(payment_value: str, entity_portfolio, entity_id):
        entity_id = int(entity_id)
        if not Validator._validate_float(payment_value):
            return False
        payment_value = float(payment_value)
        if payment_value <= 0:  #do not allow user to make a debt payment for zero dollars or negative dollars
            MainUI.MainUI.pos_num_not_given()
            return False
        #make sure the user cannot pay more into the debt than the debt itself
        #in other words: make sure the user cannot pay $200 into a $100 debt beacuse that would just be silly
        debt_entity = entity_portfolio.get_entity(entity_id)
        debt_value = debt_entity.get_single_value()
        if debt_value < payment_value:
            return False
        return True

    #use to validate user pin entry, only allow pins of length 4 and only numbers
    @staticmethod
    def validate_pin(pin: str):
        if len(pin) != 4:
            return False
        if not Validator._validate_integer(pin):
            return False
        if int(pin) < 0:
            return False #do not allow negative pins because that's just silly
        return True
    @staticmethod
    def validate_password(account: UserAccount, input_password: str):
        return account.check_password(input_password)