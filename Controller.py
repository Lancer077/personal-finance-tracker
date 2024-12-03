'''
Mason Myre

My current mood: https://www.youtube.com/watch?v=9wtvXoXh0VU
'''

import MainUI
import Validator
import Operations
import EntityPortfolio
import Entity
import Transaction
import TransactionList
import UserAccount
import CategoryList
import Category
import mysql.connector #for database


entity_portfolio = EntityPortfolio.EntityPortfolio()
transaction_list = TransactionList.TransactionList()
account = UserAccount.UserAccount()
category_list = CategoryList.CategoryList()




class Controller:

    #internal functions
    def _get_transaction_amount():
        stop = False
        while not stop:
            amount = MainUI.MainUI.get_transaction_amount() #single use principle
            stop = Validator.validate_value(amount)
        return amount
    
    def _get_date():
        stop = False
        while not stop:
            date = MainUI.MainUI.get_date()
            stop = Validator.validate_transaction_date(date)
        return date
    
    def _get_desc():
        desc = MainUI.MainUI.get_desc()
        return desc

    def _get_num_owned():
        stop = False
        while not stop:
            num_owned = MainUI.MainUI.get_num_owned()
            stop = Validator.validate_num_owned(num_owned)
        return num_owned

    def _get_entity_value():
        stop = False
        while not stop:
            value = MainUI.MainUI.get_entity_value()
            stop = Validator.validate_value(value)
        return float(value)
    
    def _get_entity_name():
        stop = False
        while not stop:
            name = MainUI.MainUI.get_entity_name()
            stop = Validator.validate_entity_name(name)
        return name
    
    def _get_new_category_name():
        stop = False
        while not stop:
            name = MainUI.MainUI.get_new_category_name(category_list.get_category_names_str())
            stop = Validator.validate_new_category_name(category_list, name)
        return name
    def _get_category_name():
        stop = False
        while not stop:
            name = MainUI.MainUI.get_category_name(category_list.get_category_names_str())
            stop = Validator.validate_category_name(category_list, name)
        return name
    def _get_stock_symbol():
        stop = False
        while not stop:
            stock = MainUI.MainUI.get_stock_symbol()
            stop = Validator.validate_stock_symbol(stock)
        return stock
    
    def _calculate_current_net_worth():
        entity_portfolio.update_values()
        net_worth = 0 #reset net worth value
        net_worth += transaction_list.get_total_income()  #add total income
        net_worth -= transaction_list.get_total_expenses() #add total expense
        net_worth += entity_portfolio.total_value
        return net_worth #now we have a complete picture of the net worth so we can just return that
    
    def new_user_setup():
        new_pass = MainUI.MainUI.create_password()  #always assume the password is valid

        new_pin = MainUI.MainUI.create_pin()
        while not Validator.validate_pin(new_pin):
            new_pin = MainUI.MainUI.invalid_pin()

        #create the account using the information input by the user
        Operations.create_user_account_operations(account, new_pass, new_pin)

        #send the user to the home screen
        Controller.home_screen()
    
    def user_login():
        password = MainUI.MainUI.get_password()

        while not Validator.validate_password(account, password):
            password = MainUI.MainUI.invalid_password()


    def home_screen():
        #display main ui text
        #get user input and make sure user input is always valid
        stop = False
        net_worth = Controller._calculate_current_net_worth()
        while(not stop):
            user_selection = MainUI.MainUI.home_screen(net_worth)
            stop = Validator.validate_home_screen_entry(user_selection)   
        selection = int(user_selection)
        match selection:
            case 1:
                Controller.income_management_menu()
            case 2:
                Controller.spending_management_menu()
            case 3: 
                Controller.asset_management_menu()
            case 4: 
                Controller.liability_management_menu()
            case 5:
                #Controller.financial_reports_menu()
                pass
            case 6:
                Controller.retrieve_transactions()
            case 7: 
                #Controller.alert_center_menu()
                pass
            case 8:
                #Controller.program_settings_menu()
                pass
            case 9:
                Controller.category_management_menu() 
            case 0:
                MainUI.MainUI.exit_adv_fi()
                exit(0)     

    def income_management_menu():
        #display the main ui text
        #get user input and ensure validity
        stop = False
        while(not stop):
            user_selection = MainUI.MainUI.income_management_menu()
            stop = Validator.validate_menu_entry(user_selection, MainUI.MainUI.INCOME_MGMT_MENU_LOW, MainUI.MainUI.INCOME_MGMT_MENU_HIGH)
        selection = int(user_selection)
        match selection:
            case 1:
                Controller.income_management_menu_add_income()
            case 2:
                Controller.income_management_menu_view_income_list()
            case 3:
                Controller.income_management_menu_remove_income()
            case 4:
                Controller.income_management_menu_categorize_income()
            case 0:
                return
        return

    
    def income_management_menu_add_income():
        MainUI.MainUI.income_management_menu_add_income()
        amount = Controller._get_transaction_amount()
        date = Controller._get_date()
        desc = Controller._get_desc()

        Operations.create_and_add_transaction(transaction_list, amount, date, desc, "income")
        MainUI.MainUI.add_transaction_success()
        return

    def income_management_menu_view_income_list():
        income_list = Operations.print_income_list(transaction_list)
        MainUI.MainUI.utility_print(income_list)
        return

    
    def income_management_menu_remove_income():
        income_list = Operations.print_income_list(transaction_list)                          #so the user can find the relevant ID

        stop = False
        while not stop:
            income_id = MainUI.MainUI.remove_transaction(income_list) 
            stop = Validator.validate_transaction_id(transaction_list, income_id, "income")

        Operations.remove_transaction(transaction_list, income_id, "income")
        return
    
    def income_management_menu_categorize_income():
        """
        oh boy time to actually categorize everything
        1. print out all of the categories
        2. print out all of our incomes, with their IDs
        3. the user can then type an income ID followed by the target category
        4. by pressing enter when nothing was typed, user will be sent back to the home screen        
        """
        #don't allow users to attempt to categorize ANY ITEMS until there are actual categories already created
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            Controller.home_screen()
        income_list = Operations.print_income_list(transaction_list)
        stop = False
        while not stop:  #get the ID of the income we are going to categorize
            income_id = MainUI.MainUI.categorize_transaction(income_list)
            stop = Validator.validate_transaction_id(transaction_list, income_id, "income")
        if income_id == "-1":
            MainUI.MainUI.action_cancelled()
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            MainUI.MainUI.action_cancelled()
            return
        #once we have both, now we will call the operator to assign the income to the category
        Operations.categorize_transaction(transaction_list, category_list, income_id, category_name, "income")
        MainUI.MainUI.categorize_transaction_success()
        return
        

    def spending_management_menu():
        #display the main ui text
        #get user input and ensure validity
        stop = False
        while(not stop):
            user_selection = MainUI.MainUI.spending_management_menu()
            stop = Validator.validate_menu_entry(user_selection, MainUI.MainUI.SPENDING_MGMT_MENU_LOW, MainUI.MainUI.SPENDING_MGMT_MENU_HIGH)
        selection = int(user_selection)
        #print(selection)
        match selection:
            case 0:
                return
            case 1: 
                Controller.spending_management_menu_add_expense()
            case 2:
                Controller.spending_management_menu_view_expense_list()
            case 3:
                Controller.spending_management_menu_delete_expense()
            case 4:
                #Controller.spending_management_menu_import_spending_CSV()
                pass
            case 5:
                Controller.spending_management_menu_categorize_expense()
            case 6:
                Controller.spending_management_menu_set_category_budget()
            case 7:
                Controller.spending_management_menu_monitor_budget_adherence()
                pass
        return
    
    def spending_management_menu_add_expense():
        MainUI.MainUI.spending_management_menu_add_expense()
        amount = Controller._get_transaction_amount()
        date = Controller._get_date()
        desc = Controller._get_desc()

        Operations.create_and_add_transaction(transaction_list, amount, date, desc, "expense")
        MainUI.MainUI.add_transaction_success()
        return
        
    def spending_management_menu_view_expense_list():
        expense_list = Operations.print_expense_list(transaction_list)
        MainUI.MainUI.utility_print(expense_list)
        return    
    
    def spending_management_menu_delete_expense():
        expense_list = Operations.print_expense_list(transaction_list)

        stop = False
        while not stop:
            expense_id = MainUI.MainUI.remove_transaction(expense_list) 
            stop = Validator.validate_transaction_id(transaction_list, expense_id, "expense")
        Operations.remove_transaction(transaction_list, expense_id, "expense")
        return
    
    #to find a more commented version, try ctrl f "categorize_income"
    def spending_management_menu_categorize_expense():
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            Controller.home_screen()
        expense_list = Operations.print_expense_list(transaction_list)
        stop = False
        while not stop:  #get the ID of the income we are going to categorize
            expense_id = MainUI.MainUI.categorize_transaction(expense_list)
            stop = Validator.validate_transaction_id(transaction_list, expense_id, "expense")
        if expense_id == "-1":
            MainUI.MainUI.action_cancelled()
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            MainUI.MainUI.action_cancelled()
            return
        Operations.categorize_transaction(transaction_list, category_list, expense_id, category_name, "expense")
        MainUI.MainUI.categorize_transaction_success()
        return
    
    def spending_management_menu_set_category_budget():
        #get category name
        #set category budget
        #print(category_list.get_category_count)
        if category_list.get_category_count() < 1:
            MainUI.MainUI.error_no_categories_budgeting()
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            MainUI.MainUI.action_cancelled()
            return
        
        stop = False
        MainUI.MainUI.get_category_budget()
        while not stop:
            category_budget = MainUI.MainUI.get_category_budget_2()
            stop = Validator.validate_value(category_budget)
        Operations.category_management_menu_set_category_budget_operations(category_list, category_name, category_budget)
        MainUI.MainUI.set_category_budget_success()


    def spending_management_menu_monitor_budget_adherence():
        #here we will go to the category list, grab all of the categories that have a budget that is not -1
        #then we will grab all of the expense transactions associated with that budget that have happened within the past month
        #then we will total up all of those expenses and display how much the user has spent
        adherence = Operations.spending_management_menu_monitor_budget_adherence_operations(category_list)
        MainUI.MainUI.utility_print(adherence)


    def asset_management_menu():
        assets_value = entity_portfolio.total_assets_value
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.asset_management_menu(assets_value)
            stop = Validator.validate_menu_entry(user_selection, MainUI.MainUI.ASSET_MGMT_MENU_LOW, MainUI.MainUI.ASSET_MGMT_MENU_HIGH)
        selection = int(user_selection)
        match selection:
            case 1:
                Controller.asset_management_menu_add_asset()
            case 2:
                Controller.asset_management_menu_view_asset_list()
            case 3:
                Controller.asset_management_menu_delete_asset()
            case 4:
                Controller.asset_management_menu_update_assets()
            case 5:
                Controller.asset_management_menu_categorize_assets()
            case 0:
                return

        
    def asset_management_menu_add_asset():
        #need num owned, value per entity, name, desc, auto update & stock symbol
        stop = False
        while not stop:
            is_stock = MainUI.MainUI.asset_management_menu_add_asset_is_stock()
            stop = Validator.validate_yes_no(is_stock)
        
        num_owned = Controller._get_num_owned()
        if num_owned == "":
            num_owned = 1
        name = Controller._get_entity_name()
        desc = Controller._get_desc()

        if is_stock[0] == "n":
            value = Controller._get_entity_value()
            auto_update = False
            stock_symbol = "n/a"
        elif is_stock[0] == "y":
            #can pass in value as 0 because we will automatically update it anyway
            value = 0
            auto_update = True #tell entity.py that this is a stock and that the symbol matters
            stock_symbol = Controller._get_stock_symbol()        
        #now that we have all the data we need to create a non stock asset, we will
        #call a method in operations to do exactly that
        Operations.add_entity_to_portfolio(entity_portfolio, "asset", name, desc, value, num_owned, auto_update, stock_symbol)
        return


    def asset_management_menu_view_asset_list():
        asset_list = Operations.asset_management_menu_view_asset_list_operations(entity_portfolio)
        MainUI.MainUI.utility_print(asset_list)
        return

    def asset_management_menu_delete_asset():
        #3
        asset_list = Operations.asset_management_menu_view_asset_list_operations(entity_portfolio)
        stop = False
        while not stop:
            id = MainUI.MainUI.asset_management_menu_delete_asset(asset_list)
            stop = Validator.validate_entity_id(entity_portfolio, "asset", id)
        #once the asset id is validated we need to actually remove the asset
        Operations.remove_entity_from_portfolio(entity_portfolio, "asset", id)
        return
    
    def asset_management_menu_update_assets():
        entity_portfolio.update_values()
        MainUI.MainUI.update_asset_values_success()
        return
    
    def asset_management_menu_categorize_assets():
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        asset_list = Operations.asset_management_menu_view_asset_list_operations(entity_portfolio) #with how many tiems I call this, it might've been smart to shorten it
        stop = False
        while not stop:
            asset_id = MainUI.MainUI.categorize_entity(asset_list)
            stop = Validator.validate_entity_id(entity_portfolio, "asset", asset_id)
        if asset_id == "-1":
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            return
        Operations.categorize_entity(entity_portfolio, category_list, asset_id, category_name, "asset")
        MainUI.MainUI.categorize_entity_success()
        return
        

    def liability_management_menu():
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.liability_management_menu()
            stop = Validator.validate_menu_entry(user_selection, MainUI.MainUI.LIABILITY_MGMT_MENU_LOW, MainUI.MainUI.LIABILITY_MGMT_MENU_HIGH)
        selection = int(user_selection)
        match selection:
                case 0:
                    return
                case 1:
                    Controller.liability_management_menu_add_liability()
                case 2:
                    Controller.liability_management_menu_view_liability_list()
                case 3:
                    Controller.liability_management_menu_make_liability_payment()
                case 4:
                    Controller.liability_management_menu_delete_liability()
                case 5:
                    Controller.liability_management_menu_track_debt()
                case 6:
                    Controller.liability_management_menu_categorize_liability()
        return

    def liability_management_menu_add_liability():
        MainUI.MainUI.liability_management_menu_add_liability()
        #since we will have no liabilies that auto update, we will not include stocks
        #anyone who is smart enough to be shorting stocks is not really our taraget audience
        num_owned = 1  #for sake of simplicity, we only allow one copy of each liability
        name = Controller._get_entity_name()
        desc = Controller._get_desc()
        value = Controller._get_entity_value()
        auto_update = False
        stock_symbol = "n/a"
        Operations.add_entity_to_portfolio(entity_portfolio, "liability", name, desc, value, num_owned, auto_update, stock_symbol)
        return

    def liability_management_menu_view_liability_list():
        liability_list = Operations.liability_management_menu_view_liability_list_operations(entity_portfolio)
        MainUI.MainUI.utility_print(liability_list)
        return
    
    def liability_management_menu_make_liability_payment():
        liability_list = Operations.liability_management_menu_view_liability_list_operations(entity_portfolio)
        stop = False
        while not stop:
            id = MainUI.MainUI.liability_management_menu_get_liability_id(liability_list)
            stop = Validator.validate_entity_id(entity_portfolio, "liability", id)
        #once we have found the corresponding liability ID
        #we get the amount that that the user has just paid into the liability
        stop = False
        while not stop:
            payment = MainUI.MainUI.get_payment_value()
            stop = Validator.validate_payment_debt(payment, entity_portfolio, id)
        #now that the payment is validated, we have to apply it to the debt
        Operations.make_liability_payment_operations(entity_portfolio, id, payment)
        return
    
    def liability_management_menu_delete_liability():
        liability_list = Operations.liability_management_menu_view_liability_list_operations(entity_portfolio)
        stop = False
        while not stop:
            id = MainUI.MainUI.liability_management_menu_get_liability_id(liability_list)
            stop = Validator.validate_entity_id(entity_portfolio, "liability", id)
        Operations.remove_entity_from_portfolio(entity_portfolio, "liability", id)
        return

    def liability_management_menu_track_debt():
        #print out each debt and how much is left to be paid
        debt_status = Operations.liability_management_menu_track_debt_operations(entity_portfolio)
        MainUI.MainUI.liability_track_debt(debt_status)
        return
    
    def liability_management_menu_categorize_liability():
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        liability_list = Operations.liability_management_menu_view_liability_list_operations(entity_portfolio) #with how many tiems I call this, it might've been smart to shorten it
        stop = False
        while not stop:
            liability_id = MainUI.MainUI.categorize_entity(liability_list)
            stop = Validator.validate_entity_id(entity_portfolio, "liability", liability_id)
        if liability_id == "-1":
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            return
        Operations.categorize_entity(entity_portfolio, category_list, liability_id, category_name, "liability")
        MainUI.MainUI.categorize_entity_success()
        return
        
        




        
    def retrieve_transactions():
        MainUI.MainUI.retrieve_transactions()
        transactions = Operations.print_transactions(transaction_list)
        MainUI.MainUI.utility_print(transactions)
        return

    
    def category_management_menu():
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.category_menu()       
            stop = Validator.validate_menu_entry(user_selection, MainUI.MainUI.LIABILITY_MGMT_MENU_LOW, MainUI.MainUI.LIABILITY_MGMT_MENU_HIGH)
        selection = int(user_selection)
        match selection:
                case 0:
                    return
                case 1:
                    Controller.category_management_menu_add_category()
                case 2:
                    Controller.category_management_menu_view_category_names()
                case 3:
                    Controller.category_management_menu_view_category_list_info()
                case 4:
                    Controller.category_management_menu_view_category_items()
                    
                case 5:
                    Controller.category_management_menu_delete_category()
    
    def category_management_menu_add_category():
        #need name and description
        #also need to ensure the name is unique
        cat_name = Controller._get_new_category_name()
        if cat_name == "-1":
            MainUI.MainUI.action_cancelled()
            return
        cat_desc = Controller._get_desc()

        
        #now that we have a name and description, we will send the data to operations
        #so that operations can create the category, then add it to the list
        Operations.category_management_menu_add_category_operations(category_list, cat_name, cat_desc)

        #let the user know that the category has been added successfully
        MainUI.MainUI.category_added_success(cat_name)
        #send user to the home screen
        return
        
    def category_management_menu_view_category_names():
        #go to the category list and grab the category name list
        category_name_list = category_list.get_category_names_str()
        #send to MainUI
        MainUI.MainUI.category_menu_show_category_names(category_name_list)
        return
    
    def category_management_menu_view_category_list_info():
        category_list_info = category_list.get_category_list_info()
        MainUI.MainUI.category_menu_show_category_list_info(category_list_info)
        return

    def category_management_menu_view_category_items():
        #get a category from the user
        category_name = Controller._get_category_name()
        #get all of the incomes, expenses, assets, and liabilities associated with that category
        category_items = Operations.category_managment_menu_view_category_items(category_list, category_name)
        MainUI.MainUI.utility_print(category_items)

    def category_management_menu_delete_category():
        #show category names to the user
        category_name_list = category_list.get_category_names_str()
        stop = False
        category_name = Controller._get_category_name()
        
        if category_name == "-1":
            MainUI.MainUI.action_cancelled()
            return
        #now we actually delete the a category associated with the given name
        Operations.category_management_menu_delete_category_operations(category_list, category_name)


def testing(test_login, test_income, test_expense, test_asset, test_stock, test_liability, test_category, test_category_2):
    if test_login:
        if account.new_user == True:  #if we have a new user
            Controller.new_user_setup()
        else:
            Controller.user_login()
    if test_income:
        Operations.create_and_add_transaction(transaction_list, "500.10", "10/10/10", "test 1", "income")
        Operations.create_and_add_transaction(transaction_list, "300.22", "10/11/10", "test 2", "income")
        Operations.create_and_add_transaction(transaction_list, "1000.12", "10/12/10", "test 3", "income")
    if test_expense:
        Operations.create_and_add_transaction(transaction_list, "48.25", "10/12/10", "Vegas Blackjack", "expense")
        Operations.create_and_add_transaction(transaction_list, "10", "10/12/10", "Put it on black (it up as red)", "expense")
    if test_asset:
        Operations.add_entity_to_portfolio(entity_portfolio, "asset", "Land", "10sq ft", "300.23", "1", False, "n/a")
    if test_stock:
        Operations.add_entity_to_portfolio(entity_portfolio, "asset", "Rivian", "bloomington car company", "0", "10", True, "rivn")
        Operations.add_entity_to_portfolio(entity_portfolio, "asset", "Amazon", "home delivery", "0", "2", True, "amzn")
    if test_liability:
        Operations.add_entity_to_portfolio(entity_portfolio, "liability", "Student Debt", "4 year university", "2000", "1", False, "n/a")
        Operations.add_entity_to_portfolio(entity_portfolio, "liability", "Car Loans", "2013 Ford Fusion", "1000", "1", False, "n/a")

    if test_category:
        Operations.category_management_menu_add_category_operations(category_list, "Default Category", "")
        Operations.category_management_menu_add_category_operations(category_list, "test", "used for testing")

    if test_category_2:
        Operations.categorize_transaction(transaction_list, category_list, "1", "test", "income")
        Operations.categorize_transaction(transaction_list, category_list, "2", "test", "income")
        Operations.categorize_transaction(transaction_list, category_list, "3", "Default Category", "income")
        Operations.categorize_transaction(transaction_list, category_list, "4", "test", "expense")
        Operations.categorize_transaction(transaction_list, category_list, "5", "Default Category", "expense")

        Operations.categorize_entity(entity_portfolio, category_list, "1", "test", "asset")
        Operations.categorize_entity(entity_portfolio, category_list, "2", "test", "asset")
        Operations.categorize_entity(entity_portfolio, category_list, "3", "Default Category", "asset")
        Operations.categorize_entity(entity_portfolio, category_list, "4", "test", "liability")
        Operations.categorize_entity(entity_portfolio, category_list, "5", "Default Category", "liability")

        


    

def main():
    #this lets us set testing conditions when we start the program
    #I'm sure that I'm not the only one who doesn't want to have to add stuff manually every time for testing
    do_testing = True  #will not do the testing, regardless of any other values (this testing variable has the highest priority)
    test_login = False
    test_income = True
    test_expense = True
    test_asset = True
    test_stock = True
    test_liability = True
    test_category = True
    test_category_2 = True #only make this true if income, expense, asset, stock, liability, and category are true also

    #now we call the method that does the testing stuff
    if do_testing:
        testing(test_login, test_income, test_expense, test_asset, test_stock, test_liability, test_category, test_category_2)

    #now we can go to the home screen with a built in user history
    while True:
        Controller.home_screen()


if __name__ == "__main__":

    main()