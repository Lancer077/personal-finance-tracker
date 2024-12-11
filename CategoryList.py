'''
Used to store all of the categories and allow for easier interfacing with them

'''

import Category
import MainUI

class CategoryList:

    def __init__(self):
        self._categories = []
        self._category_names = [] #useful for displaying all of the names
        self._category_count = 0 #doubt this will be necessary but that's what I've said about a lot of things

    def add_category(self, new_category: Category) -> None:
        self._categories.append(new_category)
        self._category_names.append(new_category.get_name())
        self._category_count += 1

    def remove_category(self, category_name: str) -> bool:
        for i in range(self._category_count): #loop through the categories looking for the matching name
            if self.category_names[i] == category_name:
                deleted_category = self._categories[i]
                deleted_category.reset_item_category_names() #fix the category names of the items that now would otherwise be associated with a nonexistent category
                self._categories.remove(deleted_category)
                self._category_names.remove(category_name)
                self._category_count -= 1
                return True
        MainUI.MainUI.category_not_found() #if we couldn't find the category, let the user know
        return False
    
    #this is used to get just the names of the categories
    def get_category_names_str(self) -> str:
        names = "Category List:\n"
        for name in self._category_names:
            names += f"{name}\n"
        return names
    
    def get_category_names(self):
        return self._category_names
    
    def get_category_names_2(self):
        return self._categories._category_name

    def get_categories(self):
        return self._categories

    #this will be used to get more of the data for each category
    def get_category_list_info(self) -> str:
        info = ""
        for category in self._categories:
            info += (f"Name: {category.get_name()}\nDescription: {category.get_description()}\nIncome Count: {category._income_count}\nExpense Count: {category._expense_count}\nAsset Count: {category._asset_count}\nLiability Count: {category._liability_count}\n\n")
        return info
    
    #only use this if we have validated the category name has been created
    def get_category(self, category_name) -> Category:
        for category in self._categories:
            if category.get_name() == category_name:
                return category
    
    def get_category_count(self) -> int:
        return self._category_count

    def get_category_items_str(self, category_name: str) -> str:
        for category in self._categories:
            if category.get_name() == category_name:
                return category.get_category_items_str()
        return "ERROR: CATEGORY NOT FOUND"            

    def monitor_budget_adherence(self) -> str:
        budget_adherence_str = "Budget Adherence:\n"
        for category in self._categories:
            if category.get_budget() != -1:  #if our budget is not -1 then it is a budgeted category
                #category_adherence = category.get_budget_adherence()
                budget_adherence_str += f"{category.get_budget_adherence()}\n"
        return budget_adherence_str
