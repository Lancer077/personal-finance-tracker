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
    
    #remove items
    def remove_asset(self, asset: Entity):
        self.asset_count -= 1
        self.asset_list.remove(asset)
        return True
    
    def remove_liability(self, liability: Entity):
        self.liability_count -= 1
        self.liability_list.remove(liability)
        return True
    
    def remove_income(self, income: Transaction):
        self.income_count -= 1
        self.income_list.remove(income)
        return True
    
    def remove_expense(self, expense: Transaction):
        self.expense_count -= 1
        self.expense_list.remove(expense)
        return True
    
    #wasn't sure what the best name for this one was but the idea is that when you delete a category from the category list
    #you also need to makes sure that the items which were previously associated with that category get the category_name field reset
    def reset_item_category_names(self):
        for income in self.income_list:
            income.set_category_name("")
        for expense in self.expense_list:
            expense.set_category_name("")
        for asset in self.asset_list:
            asset.set_category_name("")
        for liability in self.liability_list:
            liability.set_category_name("")
        return True
    
    #used to help print out all of the items associated with a given category
    def get_category_items_str(self) -> str:
        items_str = f"All items associated with the category '{self.category_name}'\n\n"
        if self.income_count > 0:
            items_str += "Income List:\n"
            for income in self.income_list:
                items_str += f"{income.print_transaction()}\n"
            items_str += "\n"
        if self.expense_count > 0:
            items_str += "Expense List:\n"
            for expense in self.expense_list:
                items_str += f"{expense.print_transaction()}\n"
            items_str += "\n"
        if self.asset_count > 0:
            items_str += "Asset List:\n"
            for asset in self.asset_list:
                items_str += f"{asset.print_entity()}"
            items_str += "\n"
        if self.liability_count > 0:
            items_str += "Liability List:\n"
            for liability in self.liability_list:
                items_str += f"{liability.print_entity()}"
        return items_str




































