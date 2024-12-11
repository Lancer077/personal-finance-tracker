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
import mysql.connector
import MySQLOperations
import IncomeReport
import SpendingReport
import FinancialHealthReport


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
            stop = Validator.Validator.validate_value(amount)
        return amount
    
    def _get_date():
        stop = False
        while not stop:
            date = MainUI.MainUI.get_date()
            stop = Validator.Validator.validate_transaction_date(date)
        return date
    
    def _get_desc():
        desc = MainUI.MainUI.get_desc()
        return desc

    def _get_num_owned():
        stop = False
        while not stop:
            num_owned = MainUI.MainUI.get_num_owned()
            stop = Validator.Validator.validate_num_owned(num_owned)
        return num_owned

    def _get_entity_value():
        stop = False
        while not stop:
            value = MainUI.MainUI.get_entity_value()
            stop = Validator.Validator.validate_value(value)
        return float(value)
    
    def _get_entity_name():
        stop = False
        while not stop:
            name = MainUI.MainUI.get_entity_name()
            stop = Validator.Validator.validate_entity_name(name)
        return name
    
    def _get_new_category_name():
        stop = False
        while not stop:
            name = MainUI.MainUI.get_new_category_name(category_list.get_category_names_str())
            stop = Validator.Validator.validate_new_category_name(category_list, name)
        return name
    def _get_category_name():
        stop = False
        while not stop:
            name = MainUI.MainUI.get_category_name(category_list.get_category_names_str())
            stop = Validator.Validator.validate_category_name(category_list, name)
        return name
    def _get_stock_symbol():
        stop = False
        while not stop:
            stock = MainUI.MainUI.get_stock_symbol()
            stop = Validator.Validator.validate_stock_symbol(stock)
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
        while not Validator.Validator.validate_new_password(new_pass):
            new_pass = MainUI.MainUI.create_password()

        new_pin = MainUI.MainUI.create_pin()
        while not Validator.Validator.validate_pin(new_pin):
            new_pin = MainUI.MainUI.invalid_pin()

        #create the account using the information input by the user
        Operations.Operations.create_user_account_operations(account, new_pass, new_pin)
        MySQLOperations.MySQLOperations.create_user_account(account)
        account.new_user = False

        #send the user to the home screen
        #Controller.home_screen()
    
    def user_login():
        password = MainUI.MainUI.get_password()
        account = MySQLOperations.MySQLOperations.get_user_account()

        while not Validator.Validator.validate_password(account, password):
            password = MainUI.MainUI.invalid_password()


    def home_screen():
        #display main ui text
        #get user input and make sure user input is always valid
        stop = False
        net_worth = Controller._calculate_current_net_worth()
        while(not stop):
            user_selection = MainUI.MainUI.home_screen(net_worth)
            stop = Validator.Validator.validate_home_screen_entry(user_selection)   
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
                Controller.financial_reports_menu()
            case 6:
                Controller.retrieve_transactions()
            case 7: 
                Controller.category_management_menu() 
                pass
            case 8:
                Controller.program_settings_menu()
                pass
            case 0:
                MainUI.MainUI.exit_adv_fi()
                exit(0)     

    def income_management_menu():
        #display the main ui text
        #get user input and ensure validity
        stop = False
        while(not stop):
            user_selection = MainUI.MainUI.income_management_menu()
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.INCOME_MGMT_MENU_LOW, MainUI.MainUI.INCOME_MGMT_MENU_HIGH)
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

        Operations.Operations.create_and_add_transaction(transaction_list, amount, date, desc, "income")
        MainUI.MainUI.add_transaction_success()
        return

    def income_management_menu_view_income_list():
        income_list = Operations.Operations.print_income_list(transaction_list)
        MainUI.MainUI.utility_print(income_list)
        return

    
    def income_management_menu_remove_income():
        #ensure that there are transaction items to be recorded
        if transaction_list.get_total_income() == 0.0:
            MainUI.MainUI.utility_print_no_clear("Error: no pre-existing incomes to delete")
            return
        income_list = Operations.Operations.print_income_list(transaction_list)                          #so the user can find the relevant ID

        stop = False
        while not stop:
            income_id = MainUI.MainUI.remove_transaction(income_list) 
            stop = Validator.Validator.validate_transaction_id(transaction_list, income_id, "income")

        MySQLOperations.MySQLOperations.delete_transaction_from_db(transaction_list, income_id, "income")
        Operations.Operations.remove_transaction(transaction_list, income_id, "income")
        return
    
    def income_management_menu_categorize_income():
        """
        oh boy time to actually categorize everything
        1. print out all of the categories
        2. print out all of our incomes, with their IDs
        3. the user can then type an income ID followed by the target category
        4. by pressing enter when nothing was typed, user will be sent back to the home screen        
        """
        #don't allow caregorization of non-existent items
        if transaction_list.get_total_income() == 0.0:
            MainUI.MainUI.utility_print_no_clear("Error: no pre-existing incomes to delete")
            return
        #don't allow users to attempt to categorize ANY ITEMS until there are actual categories already created
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        income_list = Operations.Operations.print_income_list(transaction_list)
        stop = False
        while not stop:  #get the ID of the income we are going to categorize
            income_id = MainUI.MainUI.categorize_transaction(income_list)
            stop = Validator.Validator.validate_transaction_id(transaction_list, income_id, "income")
        if income_id == "-1":
            MainUI.MainUI.action_cancelled()
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            MainUI.MainUI.action_cancelled()
            return
        #once we have both, now we will call the operator to assign the income to the category
        Operations.Operations.categorize_transaction(transaction_list, category_list, income_id, category_name, "income")
        MainUI.MainUI.categorize_transaction_success()
        return
        

    def spending_management_menu():
        #display the main ui text
        #get user input and ensure validity
        stop = False
        while(not stop):
            user_selection = MainUI.MainUI.spending_management_menu()
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.SPENDING_MGMT_MENU_LOW, MainUI.MainUI.SPENDING_MGMT_MENU_HIGH)
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
                Controller.spending_management_menu_import_spending_CSV()
            case 5:
                Controller.spending_management_menu_categorize_expense()
            case 6:
                Controller.spending_management_menu_set_category_budget()
            case 7:
                Controller.spending_management_menu_delete_category_budget()
            case 8:
                Controller.spending_management_menu_monitor_budget_adherence()
                pass
        return
    
    def spending_management_menu_add_expense():
        MainUI.MainUI.spending_management_menu_add_expense()
        amount = Controller._get_transaction_amount()
        date = Controller._get_date()
        desc = Controller._get_desc()

        Operations.Operations.create_and_add_transaction(transaction_list, amount, date, desc, "expense")
        MainUI.MainUI.add_transaction_success()
        return
    
        
    def spending_management_menu_view_expense_list():
        expense_list = Operations.Operations.print_expense_list(transaction_list)
        MainUI.MainUI.utility_print(expense_list)
        return    
    
    def spending_management_menu_delete_expense():

        expense_list = Operations.Operations.print_expense_list(transaction_list)

        stop = False
        while not stop:
            expense_id = MainUI.MainUI.remove_transaction(expense_list) 
            stop = Validator.Validator.validate_transaction_id(transaction_list, expense_id, "expense")
        MySQLOperations.MySQLOperations.delete_transaction_from_db(transaction_list, expense_id, "expense")
        Operations.Operations.remove_transaction(transaction_list, expense_id, "expense")
        return
    
    def spending_management_menu_import_spending_CSV():
        stop = False
        while not stop:
            fileName = MainUI.MainUI.spending_management_menu_import_spending_CSV()
            stop = Validator.Validator.validate_file_name(fileName)
        Operations.Operations.spending_management_menu_import_spending_CSV_operations(fileName, transaction_list)
        
        
    
    #to find a more commented version, try ctrl f "categorize_income"
    def spending_management_menu_categorize_expense():
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        expense_list = Operations.Operations.print_expense_list(transaction_list)
        stop = False
        while not stop:  #get the ID of the income we are going to categorize
            expense_id = MainUI.MainUI.categorize_transaction(expense_list)
            stop = Validator.Validator.validate_transaction_id(transaction_list, expense_id, "expense")
        if expense_id == "-1":
            MainUI.MainUI.action_cancelled()
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            MainUI.MainUI.action_cancelled()
            return
        Operations.Operations.categorize_transaction(transaction_list, category_list, expense_id, category_name, "expense")
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
            stop = Validator.Validator.validate_value(category_budget)
        Operations.Operations.category_management_menu_set_category_budget_operations(category_list, category_name, category_budget)
        MainUI.MainUI.set_category_budget_success()

    def spending_management_menu_delete_category_budget():
        """
        editing a category budget
        first, grab the category name that we are editing
        then set the budget to -1.0
        """
        if category_list.get_category_count() < 1:
            MainUI.MainUI.error_no_categories_budgeting()
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            MainUI.MainUI.action_cancelled()
            return
        Operations.Operations.category_management_menu_set_category_budget_operations(category_list, category_name, -1.0)
        MainUI.MainUI.utility_print_no_clear(f"Budget for category '{category_name}' deleted successfully")
        
    def spending_management_menu_monitor_budget_adherence():
        #here we will go to the category list, grab all of the categories that have a budget that is not -1
        #then we will grab all of the expense transactions associated with that budget that have happened within the past month
        #then we will total up all of those expenses and display how much the user has spent
        adherence = Operations.Operations.spending_management_menu_monitor_budget_adherence_operations(category_list)
        MainUI.MainUI.utility_print(adherence)


    def asset_management_menu():
        assets_value = entity_portfolio.total_assets_value
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.asset_management_menu(assets_value)
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.ASSET_MGMT_MENU_LOW, MainUI.MainUI.ASSET_MGMT_MENU_HIGH)
        selection = int(user_selection)
        match selection:
            case 1:
                Controller.asset_management_menu_add_asset()
            case 2:
                Controller.asset_management_menu_view_asset_list()
            case 3:
                Controller.asset_management_menu_edit_asset()
            case 4:
                Controller.asset_management_menu_delete_asset()
            case 5:
                Controller.asset_management_menu_update_assets()
            case 6:
                Controller.asset_management_menu_categorize_assets()
            case 0:
                return

        
    def asset_management_menu_add_asset():
        #need num owned, value per entity, name, desc, auto update & stock symbol
        stop = False
        while not stop:
            is_stock = MainUI.MainUI.asset_management_menu_add_asset_is_stock()
            stop = Validator.Validator.validate_yes_no(is_stock)
        
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
        Operations.Operations.add_entity_to_portfolio(entity_portfolio, "asset", name, desc, value, num_owned, auto_update, stock_symbol)
        MySQLOperations.MySQLOperations.add_entity_to_db("asset", name, desc, value, num_owned, auto_update, stock_symbol, entity_portfolio.next_entity_id)
        return


    def asset_management_menu_view_asset_list():
        asset_list = Operations.Operations.asset_management_menu_view_asset_list_operations(entity_portfolio)
        MainUI.MainUI.utility_print(asset_list)
        return

    def asset_management_menu_edit_asset():
        if len(entity_portfolio.get_asset_list()) == 0:
            MainUI.MainUI.utility_print_no_clear("Error: no pre-existing assets to edit")
            return
        asset_list = Operations.Operations.asset_management_menu_view_asset_list_operations(entity_portfolio)
        stop = False
        while not stop:
            id = MainUI.MainUI.asset_management_menu_edit_delete_asset(asset_list, "edit")
            stop = Validator.Validator.validate_entity_id(entity_portfolio, "asset", id)
        if id == "-1":
            MainUI.MainUI.action_cancelled()
            return
        asset_obj = Operations.Operations.get_entity(entity_portfolio, "asset", id)
        is_stock = asset_obj.get_auto_update()
        low_end = 0
        high_end = 3
        options = f"Select a value to edit for {asset_obj.get_name()}:\n1: Edit Name\n2: Edit Description\n3: Edit Amount Owned"
        if not is_stock:
            options += "\n4: Edit Individual Value"
            high_end = 4
        options += "\n0: Cancel this action"
        stop = False
        while not stop:
            selection = MainUI.MainUI.utility_print_with_return(options)
            stop = Validator.Validator.validate_menu_entry(selection, low_end, high_end)
        selection = int(selection)
        match selection:
            case 0:
                MainUI.MainUI.action_cancelled()
                return
            case 1:
                asset_obj.set_name(Controller._get_entity_name())
            case 2:
                asset_obj.set_description(Controller._get_desc())
            case 3:
                asset_obj.set_amount(Controller._get_num_owned())
            case 4:
                asset_obj.set_single_value(Controller._get_entity_value())
        MainUI.MainUI.utility_print_no_clear("Update successful!")

    def asset_management_menu_delete_asset():
        if len(entity_portfolio.get_asset_list()) == 0:
            MainUI.MainUI.utility_print_no_clear("Error: no pre-existing assets to delete")
            return
        asset_list = Operations.Operations.asset_management_menu_view_asset_list_operations(entity_portfolio)
        stop = False
        while not stop:
            id = MainUI.MainUI.asset_management_menu_edit_delete_asset(asset_list, "delete")
            stop = Validator.Validator.validate_entity_id(entity_portfolio, "asset", id)
        #once the asset id is validated we need to actually remove the asset
        Operations.Operations.remove_entity_from_portfolio(entity_portfolio, "asset", id)
        return
    
    def asset_management_menu_update_assets():
        entity_portfolio.update_values()
        MainUI.MainUI.update_asset_values_success()
        return
    
    def asset_management_menu_categorize_assets():
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        asset_list = Operations.Operations.asset_management_menu_view_asset_list_operations(entity_portfolio) #with how many tiems I call this, it might've been smart to shorten it
        stop = False
        while not stop:
            asset_id = MainUI.MainUI.categorize_entity(asset_list)
            stop = Validator.Validator.validate_entity_id(entity_portfolio, "asset", asset_id)
        if asset_id == "-1":
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            return
        Operations.Operations.categorize_entity(entity_portfolio, category_list, asset_id, category_name, "asset")
        MainUI.MainUI.categorize_entity_success()
        return
        

    def liability_management_menu():
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.liability_management_menu()
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.LIABILITY_MGMT_MENU_LOW, MainUI.MainUI.LIABILITY_MGMT_MENU_HIGH)
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
                    Controller.liability_management_menu_edit_liability()
                case 5:
                    Controller.liability_management_menu_delete_liability()
                case 6:
                    Controller.liability_management_menu_track_debt()
                case 7:
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
        Operations.Operations.add_entity_to_portfolio(entity_portfolio, "liability", name, desc, value, num_owned, auto_update, stock_symbol)
        MySQLOperations.MySQLOperations.add_entity_to_db("liability", name, desc, value, num_owned, auto_update, stock_symbol, entity_portfolio.next_entity_id)
        return

    def liability_management_menu_view_liability_list():
        liability_list = Operations.Operations.liability_management_menu_view_liability_list_operations(entity_portfolio)
        MainUI.MainUI.utility_print(liability_list)
        return
    
    def liability_management_menu_edit_liability():
        if len(entity_portfolio.get_liability_list()) == 0:
            MainUI.MainUI.utility_print_no_clear("Error: no pre-existing liabilities to edit")
            return
        liability_list = Operations.Operations.liability_management_menu_view_liability_list_operations(entity_portfolio)
        stop = False
        while not stop:
            id = MainUI.MainUI.liability_management_menu_get_liability_id(liability_list)
            stop = Validator.Validator.validate_entity_id(entity_portfolio, "liability", id)
        if id == "-1":
            MainUI.MainUI.action_cancelled()
            return
        liability_obj = Operations.Operations.get_entity(entity_portfolio, "liability", id)
        low_end = 0
        high_end = 2

        options = f"Select a value to edit for {liability_obj.get_name()}:\n1: Edit Name\n2: Edit Description\n0: Cancel this action"

        stop = False
        while not stop:
            selection = MainUI.MainUI.utility_print_with_return(options)
            stop = Validator.Validator.validate_menu_entry(selection, low_end, high_end)
        selection = int(selection)
        match selection:
            case 0:
                MainUI.MainUI.action_cancelled()
                return
            case 1:
                liability_obj.set_name(Controller._get_entity_name())
            case 2:
                liability_obj.set_description(Controller._get_desc())
        MainUI.MainUI.utility_print_no_clear("Update successful!")
    
    def liability_management_menu_make_liability_payment():
        if len(entity_portfolio.get_liability_list()) == 0:
            MainUI.MainUI.utility_print_no_clear("Error: no pre-existing liabilities to make payments towards")
            return
        liability_list = Operations.Operations.liability_management_menu_view_liability_list_operations(entity_portfolio)
        stop = False
        while not stop:
            id = MainUI.MainUI.liability_management_menu_get_liability_id(liability_list)
            stop = Validator.Validator.validate_entity_id(entity_portfolio, "liability", id)
        #once we have found the corresponding liability ID
        #we get the amount that that the user has just paid into the liability
        stop = False
        while not stop:
            payment = MainUI.MainUI.get_payment_value()
            stop = Validator.Validator.validate_payment_debt(payment, entity_portfolio, id)
        #now that the payment is validated, we have to apply it to the debt
        Operations.Operations.make_liability_payment_operations(entity_portfolio, id, payment)
        return
    
    def liability_management_menu_delete_liability():
        if len(entity_portfolio.get_liability_list()) == 0:
            MainUI.MainUI.utility_print_no_clear("Error: no pre-existing liabilities to delete")
            return
        liability_list = Operations.Operations.liability_management_menu_view_liability_list_operations(entity_portfolio)
        stop = False
        while not stop:
            id = MainUI.MainUI.liability_management_menu_get_liability_id(liability_list)
            stop = Validator.Validator.validate_entity_id(entity_portfolio, "liability", id)
        Operations.Operations.remove_entity_from_portfolio(entity_portfolio, "liability", id)
        return

    def liability_management_menu_track_debt():
        if len(entity_portfolio.get_liability_list()) == 0:
            MainUI.MainUI.utility_print_no_clear("Error: no pre-existing liabilities to track debt for")
            return
        #print out each debt and how much is left to be paid
        debt_status = Operations.Operations.liability_management_menu_track_debt_operations(entity_portfolio)
        MainUI.MainUI.liability_track_debt(debt_status)
        return
    
    def liability_management_menu_categorize_liability():
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        liability_list = Operations.Operations.liability_management_menu_view_liability_list_operations(entity_portfolio) #with how many tiems I call this, it might've been smart to shorten it
        stop = False
        while not stop:
            liability_id = MainUI.MainUI.categorize_entity(liability_list)
            stop = Validator.Validator.validate_entity_id(entity_portfolio, "liability", liability_id)
        if liability_id == "-1":
            return
        category_name = Controller._get_category_name()
        if category_name == "-1":
            return
        Operations.Operations.categorize_entity(entity_portfolio, category_list, liability_id, category_name, "liability")
        MainUI.MainUI.categorize_entity_success()
        return
        
    def financial_reports_menu():
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.financial_reports_menu()
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.FINANCIAL_REPORTS_MENU_LOW, MainUI.MainUI.FINANCIAL_REPORTS_MENU_HIGH)
        selection = int(user_selection)
        match selection:
            case 0:
                return
            case 1:
                Controller.financial_reports_menu_income_report()
            case 2:
                Controller.financial_reports_menu_spending_report()
            case 3:
                Controller.financial_reports_menu_financial_health_report()
            case 4:
                Controller.financial_reports_menu_retrieve_report()
                # MySQLOperations.MySQLOperations.get_report()
    

    def financial_reports_menu_income_report():
        # Operations.Operations.print_income_report(transaction_list)
        income_report = Operations.Operations.financial_reports_menu_report_operations("income", transaction_list)
        # MainUI.MainUI.utility_print(f"type: {type(income_report)}")
        income_report.generate_report()
        #MainUI.MainUI.financial_reports_menu_report_options("income")
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.financial_reports_menu_report_options("income")
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.FINANCIAL_REPORTS_OPTIONS_LOW, MainUI.MainUI.FINANCIAL_REPORTS_OPTIONS_HIGH)
        selection = int(user_selection)
        match selection:
            case 0:
                return
            case 1:
                MySQLOperations.MySQLOperations.add_income_report(income_report.to_string()) #REPORT!!!!
            case 2:
                Controller.export_report_to_PDF("income", income_report)
            case 3:
                MySQLOperations.MySQLOperations.add_income_report(income_report.to_string()) #REPORT!!!!
                Controller.export_report_to_PDF("income", income_report)

    
    def export_report_to_PDF(type: str, report):
        filename = MainUI.MainUI.financial_reports_menu_export_to_pdf()
        if type != "financial health":
            header = report.get_header()
            body = report.get_body()
            Operations.Operations.generate_pdf_report(filename, header, body)
        else:
            header = report.get_header()
            body = report.get_body()
            score = report.get_score()
            Operations.Operations.generate_pdf_report(filename, header, body, score)
        


    
    def financial_reports_menu_spending_report():
        spending_report = Operations.Operations.financial_reports_menu_report_operations("spending", transaction_list)
        spending_report.generate_report()
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.financial_reports_menu_report_options("spending")
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.FINANCIAL_REPORTS_OPTIONS_LOW, MainUI.MainUI.FINANCIAL_REPORTS_OPTIONS_HIGH)
        selection = int(user_selection)
        match selection:
            case 0:
                return
            case 1:
                MySQLOperations.MySQLOperations.add_spending_report(spending_report.to_string()) #REPORT!!!!
            case 2:
                Controller.export_report_to_PDF("spending", spending_report)
            case 3:
                MySQLOperations.MySQLOperations.add_health_report(spending_report.to_string()) #REPORT!!!!
                Controller.export_report_to_PDF("spending", spending_report)

                
        

    def financial_reports_menu_financial_health_report():
        financial_health_report = Operations.Operations.financial_reports_menu_report_operations("financial health", transaction_list, entity_portfolio)
        financial_health_report.generate_report()
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.financial_reports_menu_report_options("financial health")
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.FINANCIAL_REPORTS_OPTIONS_LOW, MainUI.MainUI.FINANCIAL_REPORTS_OPTIONS_HIGH)
        selection = int(user_selection)
        match selection:
            case 0:
                return
            case 1:
                MySQLOperations.MySQLOperations.add_health_report(financial_health_report.to_string()) #REPORT!!!!
            case 2:
                Controller.export_report_to_PDF("financial health", financial_health_report)
            case 3:
                MySQLOperations.MySQLOperations.add_health_report(financial_health_report.to_string()) #REPORT!!!!
                Controller.export_report_to_PDF("financial health", financial_health_report)



    def financial_reports_menu_retrieve_report():
        #MySQLOperations.MySQLOperations.get_report()
        MySQLOperations.MySQLOperations.get_income_report()
        MySQLOperations.MySQLOperations.get_spending_report()
        MySQLOperations.MySQLOperations.get_health_report()


    def retrieve_transactions():
        MainUI.MainUI.retrieve_transactions()
        transactions = Operations.Operations.print_transactions(transaction_list)
        MainUI.MainUI.utility_print(transactions)
        return

    
    def category_management_menu():
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.category_menu()       
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.LIABILITY_MGMT_MENU_LOW, MainUI.MainUI.LIABILITY_MGMT_MENU_HIGH)
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
        Operations.Operations.category_management_menu_add_category_operations(category_list, cat_name, cat_desc)

        #let the user know that the category has been added successfully
        MainUI.MainUI.category_added_success(cat_name)
        #send user to the home screen
        return
        
    def category_management_menu_view_category_names():
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        #go to the category list and grab the category name list
        category_name_list = category_list.get_category_names_str()
        #send to MainUI
        MainUI.MainUI.category_menu_show_category_names(category_name_list)
        return
    
    def category_management_menu_view_category_list_info():
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        category_list_info = category_list.get_category_list_info()
        MainUI.MainUI.category_menu_show_category_list_info(category_list_info)
        return

    def category_management_menu_view_category_items():
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        #get a category from the user
        category_name = Controller._get_category_name()
        #get all of the incomes, expenses, assets, and liabilities associated with that category
        category_items = Operations.Operations.category_managment_menu_view_category_items(category_list, category_name)
        MainUI.MainUI.utility_print(category_items)

    def category_management_menu_delete_category():
        #show category names to the user
        if category_list.get_category_count() == 0:
            MainUI.MainUI.error_no_categories_categorization()
            return
        category_name_list = category_list.get_category_names_str()
        stop = False
        category_name = Controller._get_category_name()
        
        if category_name == "-1":
            MainUI.MainUI.action_cancelled()
            return
        #now we actually delete the a category associated with the given name
        Operations.Operations.category_management_menu_delete_category_operations(category_list, category_name)


    def program_settings_menu():
        stop = False
        while not stop:
            user_selection = MainUI.MainUI.utility_print_with_return("Program Settings Menu:\n1: Change Password\n2: Program Credits\n3: Delete user account\n0: Return to main menu")
            stop = Validator.Validator.validate_menu_entry(user_selection, MainUI.MainUI.PROGRAM_SETTINGS_MENU_LOW, MainUI.MainUI.PROGRAM_SETTINGS_MENU_HIGH)
        match int(user_selection):
            case 0:
                return
            case 1:
                Controller.program_settings_menu_change_password()
            case 2:
                MainUI.MainUI.utility_print("The Adv-Fi Team:\nJaden Winterpacht\nMason Myre\nJonah Raef\nFrank Watring")
            case 3:
                MySQLOperations.MySQLOperations.delete_account()
                MainUI.MainUI.utility_print("User account was deleted")
                exit(0)
        
    def _set_new_password():
        stop = False
        while not stop:
            new_pass = MainUI.MainUI.utility_print_with_return("Please enter your new password")
            stop = Validator.Validator.validate_new_password(new_pass)
        account.set_password(new_pass)

    def program_settings_menu_change_password():
        while True:
            password_input = MainUI.MainUI.utility_print_with_return("Please enter your current password: ")
            if account.check_password(password_input):
                Controller._set_new_password()
                return
            else:
                stop = False
                while not stop:
                    user_input = MainUI.MainUI.utility_print_with_return("Incorrect password was provided, would you like to use your pin instead? (y/n)")
                    stop = Validator.Validator.validate_yes_no(user_input)
                if user_input[0] == "y":
                    #validate the pin
                    stop = False
                    while not stop:
                        user_input = MainUI.MainUI.utility_print_with_return("Please enter your pin number:\nYou can also enter -1 to cancel the password change")
                        stop = account.check_pin(user_input)
                        if user_input == "-1":
                            MainUI.MainUI.action_cancelled()
                            return
                        if not stop:
                            MainUI.MainUI.utility_print_with_return("Incorrect pin was provided")

                    Controller._set_new_password()
                    return


def testing(test_login, test_income, test_expense, test_asset, test_stock, test_liability, test_category, test_category_2):
    
    if test_income:
        Operations.Operations.create_and_add_transaction(transaction_list, "500.10", "10/10/10", "test 1", "income")
        Operations.Operations.create_and_add_transaction(transaction_list, "300.22", "10/11/10", "test 2", "income")
        Operations.Operations.create_and_add_transaction(transaction_list, "1000.12", "10/12/10", "test 3", "income")
    if test_expense:
        Operations.Operations.create_and_add_transaction(transaction_list, "48.25", "10/12/10", "Vegas Blackjack", "expense")
        Operations.Operations.create_and_add_transaction(transaction_list, "10", "10/12/10", "Put it on black (it up as red)", "expense")
    if test_asset:
        Operations.Operations.add_entity_to_portfolio(entity_portfolio, "asset", "Land", "10sq ft", "300.23", "1", False, "n/a")
    if test_stock:
        Operations.Operations.add_entity_to_portfolio(entity_portfolio, "asset", "Rivian", "bloomington car company", "0", "10", True, "rivn")
        Operations.Operations.add_entity_to_portfolio(entity_portfolio, "asset", "Amazon", "home delivery", "0", "2", True, "amzn")
    if test_liability:
        Operations.Operations.add_entity_to_portfolio(entity_portfolio, "liability", "Student Debt", "4 year university", "2000", "1", False, "n/a")
        Operations.Operations.add_entity_to_portfolio(entity_portfolio, "liability", "Car Loans", "2013 Ford Fusion", "1000", "1", False, "n/a")

    if test_category:
        Operations.Operations.category_management_menu_add_category_operations(category_list, "Default Category", "")
        Operations.Operations.category_management_menu_add_category_operations(category_list, "test", "used for testing")

    if test_category_2:
        Operations.Operations.categorize_transaction(transaction_list, category_list, "1", "test", "income")
        Operations.Operations.categorize_transaction(transaction_list, category_list, "2", "test", "income")
        Operations.Operations.categorize_transaction(transaction_list, category_list, "3", "Default Category", "income")
        Operations.Operations.categorize_transaction(transaction_list, category_list, "4", "test", "expense")
        Operations.Operations.categorize_transaction(transaction_list, category_list, "5", "Default Category", "expense")

        Operations.Operations.categorize_entity(entity_portfolio, category_list, "1", "test", "asset")
        Operations.Operations.categorize_entity(entity_portfolio, category_list, "2", "test", "asset")
        Operations.Operations.categorize_entity(entity_portfolio, category_list, "3", "Default Category", "asset")
        Operations.Operations.categorize_entity(entity_portfolio, category_list, "4", "test", "liability")
        Operations.Operations.categorize_entity(entity_portfolio, category_list, "5", "Default Category", "liability")

        


    

def main():
    #this lets us set testing conditions when we start the program
    #I'm sure that I'm not the only one who doesn't want to have to add stuff manually every time for testing
    do_testing = False  #will not do the testing, regardless of any other values (this testing variable has the highest priority)
    test_login = True
    test_income = True
    test_expense = True
    test_asset = True
    test_stock = True
    test_liability = True
    test_category = True
    test_category_2 = True #only make this true if income, expense, asset, stock, liability, and category are true also

    #before anything, check whether database connection is established
    Validator.Validator.validate_database_connection()

    #now that database connection is established, fill pull its data and store in program's memory
    MySQLOperations.MySQLOperations.pull_trans_from_database(transaction_list)
    MySQLOperations.MySQLOperations.pull_entities_from_database(entity_portfolio)
    MySQLOperations.MySQLOperations.pull_categories_from_db(category_list)
    user_exists= MySQLOperations.MySQLOperations.check_account_state()
    if user_exists:  #if we have a new user
        Controller.user_login()
        
    else:
        Controller.new_user_setup()
        MySQLOperations.MySQLOperations.set_account_state()

    #now we call the method that does the testing stuff
    if do_testing:
        testing(test_login, test_income, test_expense, test_asset, test_stock, test_liability, test_category, test_category_2)

    #now we can go to the home screen with a built in user history
    while True:
        Controller.home_screen()


if __name__ == "__main__":

    main()