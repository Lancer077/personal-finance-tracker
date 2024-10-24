'''
Author: Mason Myre
Purpose: To be used by Entity Portfolio to hold a user's assets and liabilities
Notable Things: Will not let you set auto_update to True unless 

'''



import yfinance

class Entity:

    #create all of the instance variables and give them default values
    type = "default type"
    single_value = 0.00                     # the value of one instance of the asset, useful for when a user owns multiple of the same asset
    amount = 0                              # how many instances of the asset a user owns
    real_value = 0.00                       # the value one instance of the asset multipled by the number of instances the user owns
    name = "default name"
    description = "default description"
    auto_update = False
    stock_symbol = "n/a"

    #constructor
    def __init__(self, entity_type, entity_value, entity_amount, entity_name, entity_description, entity_auto_update, entity_stock_symbol = "n/a"):  
        self.type = entity_type
        self.single_value = entity_value
        self.amount = entity_amount
        self.real_value = self.single_value * self.amount
        self.name = entity_name
        self.description = entity_description
        self.auto_update = entity_auto_update    # if an asset is set to auto-update, then we treat it like a stock

        if self.auto_update:            #handling the case that occurs when a user instantiates an asset with an invalid stock symbol
            cur_price = get_stock_value(entity_stock_symbol)
            if cur_price == None:
                self.auto_update = False
                print("Stock not found, cannot auto update")
                return False
            self.single_value = cur_price
            self.total_value = self.single_value * self.amount
            self.stock_symbol = entity_stock_symbol  # if a stock symbol is not provided, it will be assigned a default value of "n/a" 
            return True
    
    
    
    
    #getters
    def get_type(self):
        return self.type

    def get_single_value(self):
        return self.single_value
    
    def get_amount(self):
        return self.amount
    
    def get_total_value(self):
        return self.real_value
    
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description
    
    def get_auto_update(self):
        return self.auto_update
    
    def get_stock_symbol(self):
        return self.stock_symbol

    
    #setters, they return true if successful, false if unsuccessful
    def set_type(self, new_type):
        self.type = new_type
        return True
    
    def set_single_value(self, new_single_value):
        if self.auto_update:
            print("Asset is set to auto update, cannot manually modify value")
            return False
        self.single_value = new_single_value
        self.total_value = self.single_value * self.amount
        return True
    
    def set_amount(self, new_amount):
        self.amount = new_amount
        self.total_value = self.single_value * self.amount
        return True
    
    #there is no set_total_value because we should only let the user edit the value of individual assets

    def set_name(self, new_name):
        self.name = new_name
        return True
    
    def set_description(self, new_description):
        self.description = new_description
        return True
    
    def set_auto_update(self, new_auto_update, new_stock_symbol = "n/a"):
        if new_auto_update:
            if(self.stock_symbol == "n/a" and new_stock_symbol == "n/a"):  # if we want to modify the stock to allow for automatic updating, 
                print("Auto Update requires a stock symbol")               # then we need to ensure that we are getting a valid stock symbol
                return False

            cur_price = get_stock_value(new_stock_symbol)

            if cur_price == None:                                   # if the price == None, then that means the stock symbol was invalid
                print("invalid stock symbol, cannot update")
                return False

            #if we reach this part of the code, we are in a state where the user wants the stock to auto update, and the symbol is valid
            self.auto_update = new_auto_update      #now we update all of the values accordingly
            self.stock_symbol = new_stock_symbol
            self.single_value = cur_price
            self.total_value = self.single_value * self.amount

            return True         #update successful
        
        #if we are no longer auto_updating a previously auto updated asset
        #don't need any checks for this
        self.auto_update = new_auto_update  # this will always be false
        self.stock_symbol = "n/a"
        
        return True         #update successful
    

    def set_stock_symbol(self, new_stock_symbol):

        cur_price = get_stock_value(new_stock_symbol)

        if cur_price == None:
            print("invalid stock symbol, cannot update")
            return False
        
        #if the stock symbol is valid, update it accordingly
        self.single_value = cur_price
        self.total_value = self.amount * self.single_value
        return True


    def auto_update_value(self):
        if(self.auto_update):
            
            cur_price = get_stock_value(self.stock_symbol)

            if cur_price == None:
                print("invalid stock symbol, cannot update asset value until this is fixed")
                return False
            
            self.single_value = cur_price
            self.total_value = self.amount * self.single_clear
            return True
        
        print("Cannot auto update an asset that does not have the auto_update value set to true")
        return False
    

#interface to get the stock value
def get_stock_value(stock_symbol):

    stock = yfinance.Ticker(stock_symbol)
    cur_price = stock.fast_info.get("lastPrice")

    return cur_price
            
            
            

            





