class Category:
    category_name = ""
    category_description = ""

    def __init__(self, new_name, new_description):
        self.category_name = new_name
        self.category_description = new_description
    
    def get_name(self):
        return self.cetegory_name
    
    def get_description(self):
        return self.category_description
    
    def set_name(self, new_name):
        self.category_name = new_name
        return True
    
    def set_description(self, new_description):
        self.category_description = new_description