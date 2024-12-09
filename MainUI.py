import os

input_text = ""
#input_text = "Press enter to return to the main menu"

class MainUI:
    # class variables
    INCOME_MGMT_MENU_LOW = 0
    INCOME_MGMT_MENU_HIGH = 4
    SPENDING_MGMT_MENU_LOW = 0
    SPENDING_MGMT_MENU_HIGH = 8
    ASSET_MGMT_MENU_LOW = 0
    ASSET_MGMT_MENU_HIGH = 6
    LIABILITY_MGMT_MENU_LOW = 0
    LIABILITY_MGMT_MENU_HIGH = 7
    CATEGORY_MGMT_MENU_LOW = 0
    CATEGORY_MGMT_MENU_HIGH = 5
    PROGRAM_SETTINGS_MENU_LOW = 0
    PROGRAM_SETTINGS_MENU_HIGH = 2
    FINANCIAL_REPORTS_MENU_HIGH = 4
    FINANCIAL_REPORTS_MENU_LOW = 0

    def clear_screen():
        #pass
        # for Windows
        if os.name == "nt":
            os.system("cls")
        # for macOS and Linux
        else:
            os.system("clear")

    def get_transaction_amount():
        print("Enter transaction amount in dollars: ")
        return input("$")
    
    def get_date():
        print("Enter date in MM/DD/YY format:")
        return input()

    def get_desc():
        print("Enter a description: ")
        return input()
    
    def get_num_owned():
        print("Enter the number of entites you own\nWill default to 1 if left blank")
        return input()
    
    def get_entity_value():
        print("Enter the entity value:")
        return input("$")
    
    def get_entity_name():
        print("Enter the entity name:")
        return input()
    
    def get_new_category_name(category_names):
        MainUI.clear_screen()
        print(category_names)
        print("Enter the name for the new category:\nPlease note, this name must be unique as category names are not allowed to repeat\nEnter -1 if you would like to cancel this operation")
        return input()
    
    def get_category_name(category_names):
        #MainUI.clear_screen()
        print(f"\n{category_names}")
        print("Enter the name of the category you would like to associate the item with, please ensure correct spelling\nEnter -1 to cancel this operation")
        return input()
    
    def get_category_budget():
        print("Enter the monthly budget for this category:")   

    def get_category_budget_2():
        return input("$")
    
    def set_category_budget_success():
        print("Category budget successfully set")
        MainUI.wait_for_user_input()
    
    def get_stock_symbol():
        print("Enter the stock symbol that you want to link with the asset:")
        return input()

    def get_payment_value():
        print("Enter the value of the payment made towards paying off this debt: ")
        return input()

    def create_password():
        MainUI.clear_screen()
        print("Welcome to Adv-Fi, your personal finance tracker")
        print("We will start by creating a password that you will use to log in, please store this password in a safe place.")
        return input()
    
    def get_password():
        MainUI.clear_screen()
        print("Welcome back!")
        print("Please enter the password you previously set, if you forgot this password and would like to reset it, enter -1")
        return input()
    
    def invalid_password():
        print("That password was incorrect, please re-enter your password correctly or enter -1 to reset your password")
        return input()
    
    def create_pin():
        print("Here we will set up a 4 digit pin, this pin will be used to reset your password should you forget it.")
        #print("NOTE: YOU WILL BE LOCKED OUT OF YOUR ACCOUNT IF YOU FORGET BOTH YOUR PASSWORD AND PIN")
        print("NOTE: you WILL be locked out of your account if you forget both your password and pin")
        return input()
    
    def invalid_pin():
        print("That pin was not valid, please input 4 digits then press enter")
        return input()
    

    @staticmethod
    def draw_logo():
        print(r"    _      __                     ____  _____ ")
        print(r"   / \    |  \   \     /         |        |   ")
        print(r"  /---\   |   |   \   /    ===   |--      |   ")
        print(r" /     \  |__/     \_/           |      __|__ ")
        print("\n")
        return


    @staticmethod
    def show_net_worth(net_worth):
        #calculate networth and display it
        
        print(f"\nCurrent Net Worth: ${net_worth:.2f}\n")
        return
        

    @staticmethod
    def home_screen(net_worth):
        MainUI.clear_screen()
        print("\n\tWelcome to")
        MainUI.draw_logo()
        MainUI.show_net_worth(net_worth)
        print("1: Income Management Menu")
        print("2: Spending and Expense Management Menu")
        print("3: Asset Management Menu")
        print("4: Liability and Debt Management Menu")
        print("5: Financial Reports Menu")
        print("6: Retrieve Transactions")
        print("7: Category Menu")
        print("8: Program Settings Menu")
        print("0: Exit AdvFi")
        return input()

    @staticmethod
    def income_management_menu():
        MainUI.clear_screen()
        print("Income Management Menu\n----------------------------------")
        print("1: Add income")
        print("2: View income list")
        print("3: Delete income")
        print("4: Categorize incomes")
        print("0: Return to main menu")
        return input()
    
    @staticmethod
    def income_management_menu_add_income():
        MainUI.clear_screen()
        print("Adding New Income \n")
        return

    #used to print whatever you pass in, does not add anything
    #perfect for printing incomes, expenses, and reminders not to text your ex
    @staticmethod
    def utility_print(info: str):
        MainUI.clear_screen()
        print(info)
        MainUI.wait_for_user_input()

    @staticmethod
    def utility_print_no_clear(info: str) -> None:
        print(info)
        MainUI.wait_for_user_input()
        
    @staticmethod
    def utility_print_with_return(info:str) -> str:
        MainUI.clear_screen()
        print(info)
        return input()

    
    @staticmethod
    def categorize_transaction(transaction_list: str):
        MainUI.clear_screen()
        print(transaction_list)
        print("Enter the ID of the transaction you would like to categorize\nEnter -1 to cancel this operation")
        return input()

    @staticmethod
    def categorize_transaction_success():
        print("Transaction categorized successfully!")
        MainUI.wait_for_user_input()
    
    @staticmethod
    def categorize_entity(entity_list: str):
        MainUI.clear_screen()
        print(entity_list)
        print("Enter the ID of the item you would like to categorize\nEnter -1 to cancel this operation")
        return input()
    
    @staticmethod
    def categorize_entity_success():
        print("Item categorized successfully!")
        MainUI.wait_for_user_input()

    @staticmethod
    def remove_transaction(transaction_list: str):
        MainUI.clear_screen()
        print(transaction_list)
        print("\nEnter the ID of the transaction you would like to remove\nEnter -1 to cancel the operation")
        return input()

    
    @staticmethod
    def spending_management_menu():
        MainUI.clear_screen()
        print("\nSpending and Expense Management Menu")
        print("1: Add expense")
        print("2: View expense list")
        print("3: Delete expense")
        print("4: Import spending data from CSV")
        print("5: Categorize expenses")
        print("6: Set/Edit budgets for spending categories")
        print("7: Delete category budgets")
        print("8: Monitor budget adherence")
        print("0: Return to main menu")
        
        # return the user's input and give it to the Controller class
        return input()
    
    @staticmethod
    def spending_management_menu_add_expense():
        MainUI.clear_screen()
        print("Adding New Expense\n")

    @staticmethod
    def spending_management_menu_import_spending_CSV() -> str:
        MainUI.clear_screen()
        print("Enter the name of the CSV File\n")
        file = input()
        return file

    @staticmethod
    def asset_management_menu(assets_value: float):
        MainUI.clear_screen()
        print("Asset Management Menu\n")
        print(f"Current total value of assets: ${assets_value}\n")
        print("1: Add asset")
        print("2: View asset list")
        print("3: Edit Asset")
        print("4: Remove asset")
        print("5: Calculate real time asset prices")
        print("6: Categorize assets")
        print("0: Return to main menu")
        return input()
    
    @staticmethod
    def asset_management_menu_add_asset_is_stock():
        MainUI.clear_screen()
        print("Adding New Asset")
        print("Would you like to link this asset with a stock? (y/n)")
        return input()
    
    def asset_management_menu_edit_delete_asset(asset_list: str, action: str):
        MainUI.clear_screen()
        print(asset_list)
        print(f"\nEnter the ID of the asset you would like to {action}\nEnter -1 to cancel the operation")
        return input()

    
    @staticmethod
    def liability_management_menu():
        MainUI.clear_screen()
        print("\nLiability and Debt Managment Menu")
        print("1: Add liability")
        print("2: View liability list")
        print("3: Make a payment towards a liability")
        print("4: Edit liability")
        print("5: Remove liability")
        print("6: Track outstanding debt and payment debt") 
        print("7: Categorize liabilities")
        print("0: Return to main menu")
        return input()
    
    @staticmethod
    def liability_management_menu_add_liability():
        MainUI.clear_screen()
    
    @staticmethod
    def liability_management_menu_get_liability_id(liability_list):
        MainUI.clear_screen()
        print(liability_list)
        print("Enter the ID of the desired liability:")
        return input()

    @staticmethod
    def financial_reports_menu():
        MainUI.clear_screen()
        print("\nFinancial Reports Menu")
        print("1: Generate income report")              # when the user generates a report, they will be prompted to save to database, save to pdf, or both
        print("2: Generate spending report")
        print("3: Generate financial health report")
        print("4: Retrieve previously generated report from the database")  # goes to a sub-menu where all previously saved reports show up, maybe only display this option if user previously saved report to database
        print("0: Return to main menu")
        return input()
    
    @staticmethod
    def financial_reports_menu_export_to_pdf():
        MainUI.clear_screen()
        print("Enter the name of the file you want saved\n")
        file = input()
        return file
    
    @staticmethod
    def financial_reports_menu_report_options(report_type: str):
        MainUI.clear_screen()
        print(f"1: Save {report_type} report to database")
        print(f"2: Save {report_type} report as PDF")
        print(f"3: Save {report_type} report to database and as PDF")
        print(f"0: Exit without saving report")
        return input()

    @staticmethod
    def retrieve_transactions():
        MainUI.clear_screen()
        print("\nTransactions")

    @staticmethod
    def program_settings_menu():
        MainUI.clear_screen()
        print("\nProgram Settings Menu:")
        print("1: change password")
        print("2: delete user account")
        print("0: Return to main menu")

    @staticmethod
    def category_menu():
        MainUI.clear_screen()
        print("\nCategory Menu:")
        print("1: Add a new category")
        print("2: View all current category names")
        print("3: View all current categories with their number of associated transactions and entites")
        print("4: View all transactions, assets, and liabilities that are associated with a given transaction")
        print("5: Delete a category")
        print("0: Return to main menu")
        return input()

    @staticmethod
    def category_menu_show_category_names(name_list: str) -> None:
        MainUI.clear_screen()
        print(name_list)
        MainUI.wait_for_user_input()        

    @staticmethod
    def category_menu_show_category_list_info(category_list_info: str) -> None:
        MainUI.clear_screen()
        print(category_list_info)
        MainUI.wait_for_user_input()
    
    @staticmethod
    def category_menu_delete_category(category_list_info: str) -> None:
        MainUI.clear_screen()
        print(category_list_info)
        print("Enter a category name to delete, please ensure correct spelling\nEnter -1 to cancel this operation")
        return input()
    @staticmethod
    def category_menu_delete_category_success(deleted_category_name: str) -> None:
        print(f"Category '{deleted_category_name}' was deleted successfully")
        MainUI.wait_for_user_input()

    #other misc classes

    #this is used to make the program wait for the user to be ready for another action
    #typically used before going back to the home screen
    def wait_for_user_input():
        return input(input_text) #don't actually need to return anything
    
    def account_creation_success():
        print("Account created successfully!")
        MainUI.wait_for_user_input()

    def add_transaction_success():
        print("Transaction added successfully!")
        MainUI.wait_for_user_input()

    def remove_transaction_success():
        print("Transaction removed successfully!")
        MainUI.wait_for_user_input()

    
    def remove_transaction_failure(transaction_id: int):
        print(f"Transaction ID {transaction_id} was not found in the given list, nothing was removed")

    
    def action_cancelled():
        print("Action was cancelled")
        MainUI.wait_for_user_input()


    def empty_name():
        print("Error: cannot enter an empty name")

    def add_entity_success(entity_type: str): #should only ever be asset or liability
        print(f"{entity_type} added successfully") #asset/liability added successfully
        MainUI.wait_for_user_input()

    def stock_not_found(stock: str):
        print(f"{stock} was not found, please ensure correct spelling and that the stock is listed in yahoo finance\nAlso please ensure you are connected to the internet")
        

    def remove_entity_success(entity_type: str):
        print(f"{entity_type} removed successfully")
        MainUI.wait_for_user_input()

    def exit_adv_fi():
        print("Thank you for using AdvFi!")

    def update_asset_values_success():
        #MainUI.clear_screen()
        print("All values have been updated with the most up-to-date prices")
        MainUI.wait_for_user_input()

    def integer_not_given():
        print("Please be sure to enter an integer")
        

    def float_not_given():
        print("Please be sure to enter a number")
    
    def pos_num_not_given():
        print("Please be sure to enter a number that is larger than zero")

    def liability_payment_success(amount_paid: float, amount_left: float):
        print(f"Sucessfully paid ${amount_paid}, ${amount_left} left to pay")
        MainUI.wait_for_user_input()

    def liability_track_debt(debt_status: str) -> None:
        MainUI.clear_screen()
        print("Debt Tracking\n")
        print(debt_status)

        MainUI.wait_for_user_input()

    def category_name_already_exists(cat_name: str) -> None:
        print(f"The category name '{cat_name}' is already in use, please provide a new name or delete/modify the old one")
        MainUI.wait_for_user_input()
    
    def category_added_success(cat_name:str) -> None:
        print(f"The category {cat_name} was added successfully")
        MainUI.wait_for_user_input()

    def category_not_found() -> None:
        #MainUI.clear_screen()
        print("The provided category name could not be found, please ensure correct spelling and capitalization")
        MainUI.wait_for_user_input()

    def invalid_selection_range(low_end: int, high_end: int) -> None:
        print("Please enter an integer between {} and {}".format(low_end, high_end))
        MainUI.wait_for_user_input()

    def error_no_categories_categorization():
        print("ERROR: You cannot complete this action without first creating a category using the category menu")
        MainUI.wait_for_user_input()

    def error_no_categories_budgeting():
        print("ERROR: You cannot set/edit category budget without first creating a category using the category menu")
        MainUI.wait_for_user_input()

    
