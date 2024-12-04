import MainUI
import Transaction
from datetime import datetime as dt
import TransactionList
import Entity
import EntityPortfolio
import UserAccount
import Category
import CategoryList
import mysql.connector #allows Python to talk to MySQL database


def create_user_account_operations(account: UserAccount, password: str, pin: str):
    account.new_user = False
    account.set_password(password)
    account.set_pin(pin)
    


def create_and_add_transaction(transaction_list: TransactionList, amount, date, desc, type: str):
    amount = float(amount)
    date = dt.strptime(date, '%m/%d/%y')

    transaction = Transaction.Transaction(amount, date, desc)

    if type == "income":
        transaction_list.add_income_transaction(transaction)
        #Now, store the income transaction into the database
        add_income_to_database(transaction)

    
    elif type == "expense":
        transaction_list.add_expense_transaction(transaction)
    
    else:
        print("error")
    
def remove_transaction(transaction_list, transaction_id, type: str):
    transaction_id = int(transaction_id)
    #allow for the user to cancel the action
    if transaction_id == -1:
        MainUI.MainUI.action_cancelled()
        return

    found_id = False
    if type == "income":
        found_id = transaction_list.remove_income_transaction(transaction_id)
    elif type == "expense":
        found_id = transaction_list.remove_expense_transaction(transaction_id)
    
    if found_id:
        MainUI.MainUI.remove_transaction_success()
    else:
        MainUI.MainUI.remove_transaction_failure(transaction_id)

def retrieve_transaction_count(transaction_list):
    return transaction_list.get_transaction_count()

def categorize_transaction(transaction_list: TransactionList, category_list: CategoryList, transaction_id: str, category_name: str, type: str):
    category = category_list.get_category(category_name)
    transaction = transaction_list.get_transaction(transaction_id)
    if transaction.get_category_name() != "":
        old_category = category_list.get_category(transaction.get_category_name())
    if type == "income":
        category.add_income(transaction)
    elif type == "expense":
        category.add_expense(transaction)
    transaction.set_category_name(category_name)

def categorize_entity(entity_list: EntityPortfolio, category_list: CategoryList, entity_id: str, category_name: str, type: str) -> None:
    category = category_list.get_category(category_name)
    entity = entity_list.get_entity(entity_id)
    #we have this part here to ensure that when you recategorize an entity, it is removed from the previous category
    if entity.get_category_name() != "":
        old_category = category_list.get_category(entity.get_category_name())
        if type == "asset":
            old_category.remove_asset(entity)
        elif type == "liability":
            old_category.remove_liability(entity)
        
    if type == "asset":
        category.add_asset(entity)
    elif type == "liability":
        category.add_liability(entity)
    entity.set_category_name(category_name)


def asset_management_menu_view_asset_list_operations(entity_portfolio):
    return entity_portfolio.print_assets()

def liability_management_menu_view_liability_list_operations(entity_portfolio):
    return entity_portfolio.print_liabilities()


'''
type: string used to determine if entity is asset or liability

'''
def add_entity_to_portfolio(entity_portfolio, type: str, name, desc, value, num_owned, auto_update: bool, stock_symbol: str):
    #first we need to create the entity
    value = float(value)
    num_owned = int(num_owned)
    new_entity = Entity.Entity(value, num_owned, name, desc, auto_update, stock_symbol)

    #now we need to add it to the respective list
    if type == "asset":
        entity_portfolio.add_asset(new_entity)
    elif type == "liability":
        entity_portfolio.add_liability(new_entity)
        
    MainUI.MainUI.add_entity_success(type)



def remove_entity_from_portfolio(entity_portfolio, type, entity_id):
    #since we have already checked to make sure that the entity id is in the respective list,
    #we do not need to worry about that
    entity_id = int(entity_id)

    if entity_id == -1:
        MainUI.MainUI.action_cancelled()
        return

    if type == "asset":
        entity_portfolio.remove_asset(entity_id)

    elif type == "liability":
        entity_portfolio.remove_liability(entity_id)
    
    MainUI.MainUI.remove_entity_success(type)

def make_liability_payment_operations(entity_portfolio, entity_id, payment_amount):
    liability = entity_portfolio.get_entity(entity_id)
    payment_amount = float(payment_amount)
    new_entity_value = entity_portfolio.make_liability_payment(liability, payment_amount)
    entity_portfolio.total_value += payment_amount
    entity_portfolio.total_liabilities_value -= payment_amount
    MainUI.MainUI.liability_payment_success(payment_amount, new_entity_value)
    return entity_portfolio

def liability_management_menu_track_debt_operations(entity_portfolio):
    debt_status = entity_portfolio.get_debt_status()
    return debt_status


def category_management_menu_add_category_operations(category_list, new_cat_name, new_cat_desc):
    #create a new category using the provided information
    new_cat = Category.Category(new_cat_name, new_cat_desc)
    #add that new category to the list
    category_list.add_category(new_cat)
    return

def category_managment_menu_view_category_items(category_list:CategoryList, cat_name:str) -> str:
    return category_list.get_category_items_str(cat_name)

def category_management_menu_delete_category_operations(category_list: CategoryList, cat_name: str) -> None:
    category_list.remove_category(cat_name)
    MainUI.MainUI.category_menu_delete_category_success(cat_name)
    return

def category_management_menu_set_category_budget_operations(category_list: CategoryList, cat_name: str, budget: str) -> None:
    category = category_list.get_category(cat_name)
    category.set_budget(budget)
    return

def spending_management_menu_monitor_budget_adherence_operations(category_list: CategoryList) -> str:
    return category_list.monitor_budget_adherence()
    

def print_transactions(transaction_list:TransactionList) -> str:
    transactions = transaction_list.print_transactions()
    return transactions


def print_income_list(transaction_list):
    return transaction_list.print_incomes()

def print_expense_list(transaction_list):
    return transaction_list.print_expenses()


def add_income_to_database(income_transaction: Transaction):
    #first, open database connection (need to VALIDATE connection somewhere else first?)
    db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
    db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
    add_income_query = ("INSERT INTO income (amount, transaction_date, trans_desc, category_name) "
                    "VALUES (%s, %s, %s, %s)") # '%s' is a SQL.connector placeholder for ANY datatype...so we WIN!
    new_income_data = (income_transaction.Transaction.get_amount(), income_transaction.Transaction.get_transaction_date(),
                       income_transaction.Transaction.get_description(), income_transaction.Transaction.get_category_name() )
                        #add in income_transaction.Transaction.get_id once you id to the database table

    #add the data to database using the above query
    db_cursor.execute(add_income_query, new_income_data) #execute() sends query to the SQL database server for execution
    db.commit() #commit() saves changes, made by cursor(), into the database

    #close database connection; avoid any possible trouble because we good programmer
    db_cursor.close()
    db.close()