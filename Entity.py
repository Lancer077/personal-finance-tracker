'''
Author: Mason Myre
Purpose: To be used by Entity Portfolio to hold a user's assets and liabilities
Notable Things: Will not let you set auto_update to True unless given a valid ticker symbol
                
'''




import Stock
import StockFactory

class Entity:

    #constructor                          #change to enum
    def __init__(self, entity_value:float, entity_amount:int, entity_name:str, entity_description, entity_auto_update, entity_stock_symbol):  
        self._single_value = entity_value
        if entity_amount == "":
            self._amount = 1
        else:
            self._amount = int(entity_amount)
        self._real_value = self._single_value * self._amount
        self._name = entity_name
        self._description = entity_description
        self._auto_update = entity_auto_update    # if an asset is set to auto-update, then we treat it like a stock

        if self._auto_update:            #handling the case that occurs when a user instantiates an asset with an invalid stock symbol
            if not self.check_valid_symbol(entity_stock_symbol):
                self._auto_update = False
                print("Stock not found, cannot auto update")
            self.stock = StockFactory.get_stock(entity_stock_symbol)
            cur_price = self.stock.get_stock_price()
            self._single_value = cur_price
            self._total_value = self._single_value * self._amount
            self._stock_symbol = entity_stock_symbol  # if a stock symbol is not provided, it will be assigned a default value of "n/a" 
            
        self._entity_id = -1
        self._initial_value = self._single_value #only to be used by liabilities to help track how much has been paid
    
        self._category_name = ""
    
    
    #getters
    def get_entity_id(self):
        return self._entity_id

    def get_single_value(self):
        return self._single_value
    
    def get_amount(self):
        return self._amount
    
    def get_total_value(self):
        if(self._auto_update):
            self._single_value = self.stock.get_stock_price()
            self._real_value = self._amount * self._single_value
        return self._real_value
    
    def get_name(self):
        return self._name

    def get_description(self):
        return self._description
    
    def get_auto_update(self):
        return self._auto_update
    
    def get_stock_symbol(self):
        return self._stock_symbol
    
    #it would be pretty cool if we could get these to line up, but it's not a high priority
    def print_entity(self):
        id = f"ID: {self._entity_id}\t\t"
        name = f"Name: {self._name}\t\t"
        if self._amount == 1:
            value = f"Value: ${self._single_value:.2f}\t\t"
        else:
            value = f"Value: ${self._single_value:.2f}\t\tOwned: {self._amount}\t\tTotal Value: ${self._real_value:.2f}\t\t"
        desc = f"Desc: {self._description}"
        entity_info = f"{id}{name}{value}"
        if self._auto_update == True:
            entity_info += f"Stock Symbol: {self._stock_symbol}\t\t"
        if self._category_name != "":
            entity_info += f"Category: {self._category_name}\t\t"
        entity_info += f"{desc}\n"
        return entity_info

    def set_category_name(self, cat_name):
        self._category_name = cat_name
    
    def get_category_name(self) -> str:
        return self._category_name
    
    #setters, they return true if successful, false if unsuccessful, 
    def set_entity_id(self, entity_id):
        if self._entity_id == -1:
            self._entity_id = entity_id
            return True
        else:
            print("entity ID was already assigned, cannot assign a new one")
            return False
    
    def set_single_value(self, new_single_value):
        if self._auto_update:
            print("Asset is set to auto update, cannot manually modify value")
            return False
        self._single_value = new_single_value
        self._total_value = self._single_value * float(self._amount)
        return True
    
    def set_amount(self, new_amount):
        self._amount = new_amount
        self._total_value = self._single_value * self._amount
    
    #there is no set_total_value because we should only let the user edit the value of individual assets

    def set_name(self, new_name):
        self._name = new_name
    
    def set_description(self, new_description):
        self._description = new_description
    
    def set_auto_update(self, new_auto_update, new_stock_symbol = "n/a"):
        if new_auto_update:
            if(self._stock_symbol == "n/a" and new_stock_symbol == "n/a"):  # if we want to modify the stock to allow for automatic updating, 
                print("Auto Update requires a stock symbol")               # then we need to ensure that we are getting a valid stock symbol
                return False
            if self.check_valid_symbol(new_stock_symbol):                                   # if the price == None, then that means the stock symbol was invalid
                print("invalid stock symbol, cannot update")
                return False
            cur_price = self.get_stock_value(new_stock_symbol)
            #if we reach this part of the code, we are in a state where the user wants the stock to auto update, and the symbol is valid
            self._auto_update = new_auto_update      #now we update all of the values accordingly
            self._stock_symbol = new_stock_symbol
            self._single_value = cur_price
            self._total_value = self._single_value * self._amount
            return True         #update successful
        #if we are no longer auto_updating a previously auto updated asset
        #don't need any checks for this
        self._auto_update = new_auto_update  # this will always be false
        self._stock_symbol = "n/a"
        return True         #update successful
    

    def set_stock_symbol(self, new_stock_symbol):
        if self.check_valid_symbol(new_stock_symbol):
            print("invalid stock symbol, cannot update")
            return False
        
        cur_price = self.get_stock_value(new_stock_symbol)
        #if the stock symbol is valid, update it accordingly
        self._single_value = cur_price
        self._total_value = self._amount * self._single_value
        return True


    def auto_update_value(self):
        if(self._auto_update):
            if cur_price == None:
                print("invalid stock symbol, cannot update asset value until this is fixed")
                return False
            cur_price = self.get_stock_value(self._stock_symbol)
            self._single_value = cur_price
            self._total_value = self._amount * self._single_value
            return True
        print("Cannot auto update an asset that does not have the auto_update value set to true")
        return False
    
    def check_valid_symbol(self, stock_symbol: str) -> bool:
        is_stock = StockFactory.check_valid_stock_symbol(stock_symbol)
        return is_stock

    
    def get_stock_value(self, stock_symbol: str) -> float:
        price = self.stock.get_stock_price(stock_symbol)
        return price
            

            





