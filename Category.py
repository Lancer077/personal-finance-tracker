'''
Author: Mason Myre
Purpose: to be used by entity and transaction to keep track of different spending/income/asset/liability categories
Time to work on the part of this program that has given me the most headaches
(aside from the factory reporting stuff but I'm just pretending that doesn't exist for now)

Here's how this will work: we're gonna have a parent called CategoryList.py that will hold a list of the categories
    This will also have all of the methods/functions we want
    Each instance of a category will have 4 lists the assets, liabilities, incomes, and expenses associated with that category
    Each asset/liability/income/expense will also have a string varaible for the category name that can be displayed when printing out the information


'''

#11-5: updated to be compatible with associated use cases && added params to __init__

import Transaction
import Entity

class Category:

    def __init__(self, name, description = ""): 
        self.category_name = name
        self.category_description = description

        self.asset_list = []
        self.liability_list = []
        self.income_list = []
        self.expense_list = []

        self.asset_count = 0
        self.liability_count = 0
        self.income_count = 0
        self.expense_count = 0

        
    
    def get_name(self):
        return self.category_name
    
    def get_description(self):
        return self.category_description
    
    def set_name(self, new_name):
        self.category_name = new_name
        return True
    
    def set_description(self, new_description):
        self.category_description = new_description
        return True
    
    def add_asset(self, asset: Entity):
        self.asset_count += 1
        self.asset_list.append(asset)
        return True
    
    def add_liability(self, liability: Entity):
        self.liability_count += 1
        self.liability_list.append(liability)
        return True
    
    def add_income(self, income: Transaction):
        self.income_count += 1
        self.income_list.append(income)
        return True
    
    def add_expense(self, expense: Transaction):
        self.expense_count += 1
        self.expense_list.append(expense)
        return True


































