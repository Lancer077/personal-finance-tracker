#user interface updated

import Validator

class MainUI:

    @staticmethod
    def draw_logo():
        print(r"    _      __                     ____  _____ ")
        print(r"   / \    |  \   \     /         |        |   ")
        print(r"  /---\   |   |   \   /    ===   |--      |   ")
        print(r" /     \  |__/     \_/           |      __|__ ")
        print("\n")


    @staticmethod
    def show_net_worth():
        #calculate networth and display it
        net_worth = 20,000
        print("\nCurrent Net Worth: $20,000\n")
        

    @staticmethod
    def home_screen():
        
        print("\n\t\tWelcome to")
        MainUI.draw_logo()
        MainUI.show_net_worth()
        print("1: Income Management Menu")
        print("2: Spending and Expense Management Menu")
        print("3: Asset Management Menu")
        print("4: Liability and Debt Management Menu")
        print("5: Fiancial Reports Menu")
        print("6: Retrieve Transactions")
        print("7: Alert Center Menu")
        print("8: Program Settings Menu")
        print("9: Exit AdvFi")

        stop = False
        while(not stop):
            user_selection = input()
            stop = Validator.validate_home_screen_entry(user_selection)


    @staticmethod
    def income_management_menu():
        print("Income Management Menu")
        print("1: Add income")
        print("2: View income list")
        print("3: Delete income")
        print("0: Return to main menu")

    @staticmethod
    def spending_managment_menu():
        print("Spending and Expense Management Menu")
        print("1: Add expense")
        print("2: Import spending data from CSV")
        print("3: Create recurring expenses")
        print("4: Create new spending category")
        print("5: Set budgets for spending categories")
        print("6: Monitor budget adherence")
        print("7: Delete transaction")
        print("0: Return to main menu")

    @staticmethod
    def asset_management_menu():
        print("Asset Management Menu")
        print("1: Add asset")
        print("2: Remove asset")
        print("3: Calculate real time asset prices")
        print("4: Add category for assets/liabilities")
        print("0: Return to main menu")

    @staticmethod
    def liability_management_menu():
        print("Liability and Debt Managment Menu")
        print("1: Add Liability")
        print("2: Remove Liability")
        print("3: Track outstanding debt and payment debt") #will allow user to make a payment and reduce the debt recorded in AdvFi
        print("4: Add category for assets/liabilities")
        print("0: Return to main menu")

    @staticmethod
    def financial_reports_menu():
        print("Financial Reports Menu")
        print("1: Generate income report")              # when the user generates a report, they will be prompted to save to database, save to pdf, or both
        print("2: Generate spending report")
        print("3: Generate financial health report")
        print("4: Retrieve previously generated report from the database")  # goes to a sub-menu where all previously saved reports show up, maybe only display this option if user previously saved report to database
        print("0: Return to main menu")

    @staticmethod
    def retrieve_transactions():
        print("Transactions")
        print("Placeholder")
        print("0: Return to main menu")


    @staticmethod
    def alert_center_menu():
        print("Alert Center Menu")
        print("1: Create alert")
        print("2: Delete alert")
        print("3: Edit alert")
        print("4: Retrieve current alerts")
        print("5: Dismiss alert")
        print("0: Return to main menu")


    @staticmethod
    def program_settings_menu():
        print("Program Settings Menu")
        print("1: change password")
        print("2: delete user account")
        print("0: Return to main menu")


#will need to add functionality to create account/login
if __name__ == "__main__":
    MainUI.home_screen()
    pass
    