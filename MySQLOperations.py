import mysql.connector
import Transaction
import TransactionList
import Entity
import EntityPortfolio
import CategoryList
import Category
import UserAccount
import MainUI #need for util print
#import time #for debugging


class MySQLOperations:
    '''
    WARNING: This function will CRASH the program if you're not on at least: mysql-connector version 2.2.9
    Run in bash: pip install --upgrade mysql-connector-python
    'type' determines what Transaction type (income or expense) we are handling
    '''
    def add_transaction_to_database(the_transaction: Transaction, type: str):
        #Validator.validate_database_connection() proves that db connection is established. But, keep try-catch in case of unforseen failure?
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            add_income_query = ("INSERT INTO income (amount, transaction_date, trans_desc, category_name, id) "
                            "VALUES (%s, %s, %s, %s, %s)") # '%s' is a SQL.connector placeholder for ANY datatype...so we WIN!
            
            add_expense_query = ("INSERT INTO expense (amount, transaction_date, trans_desc, category_name, id) "
                                "VALUES (%s, %s, %s, %s, %s)")
            
            new_transaction_data = (the_transaction.get_amount(), the_transaction.get_transaction_date(),
                            the_transaction.get_description(), the_transaction.get_category_name(), the_transaction.get_transaction_id() )

            if type == "income":
                #add the data to database using the above query
                db_cursor.execute(add_income_query, new_transaction_data) #execute() sends query to the SQL database server for execution
            else: #type == "expense"
                db_cursor.execute(add_expense_query, new_transaction_data)

            db.commit() #commit() saves changes, made by cursor(), into the database

            #close database connection; avoid any possible trouble because we good programmer
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not store income to database. Error: {e}")
            return False #added bools for testing
        return True


    def pull_trans_from_database(transaction_list: TransactionList):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            db_cursor.execute("SELECT * FROM income")
            incomes = db_cursor.fetchall()

            #go through each attribute, income-by-income
            for row in incomes:
                amount = row[0]
                trans_date = row[1]
                desc = row[2]
                category_name = row[3]
                trans_id = row[4]

                #add transaction to the transaction_list
                trans = Transaction.Transaction(amount, trans_date, desc) #limits of Transaction.__init__
                trans.set_category_name(category_name)
                trans.set_transaction_id(trans_id)
                transaction_list.add_income_transaction(trans, True)



            '''EXPENSES'''
            db_cursor.execute("SELECT * FROM expense")
            incomes = db_cursor.fetchall()
            #go through each attribute, income-by-income
            for row in incomes:
                amount = row[0]
                trans_date = row[1]
                desc = row[2]
                category_name = row[3]
                trans_id = row[4]

                #add transaction to the transaction_list
                trans = Transaction.Transaction(amount, trans_date, desc) #limits of Transaction.__init__
                trans.set_category_name(category_name)
                trans.set_transaction_id(trans_id)
                transaction_list.add_expense_transaction(trans, True)

            #close database connection
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not grab income to database Please exit AdvFi and fix to save your data. Error: {e}")
            return False #added bools for testing
        return True

    def delete_transaction_from_db(transaction_list: TransactionList, id: str, type: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            del_income_query = ("DELETE FROM income WHERE id = %s")
            del_expense_query = ("DELETE FROM expense WHERE id = %s")

            if type == "income":
                #add the data to database using the above query
                db_cursor.execute(del_income_query, (id,)) #execute() sends query to the SQL database server for execution
            else: #type == "expense"
                db_cursor.execute(del_expense_query, (id,)) #passing 'id' as a 'tuple' to make .execute() func happy

            db.commit() #commit() saves changes, made by cursor(), into the database

            #close database connection; avoid any possible trouble because we good programmer
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not remove transaction from database. Error: {e}")
            return False #added bools for testing
        return True



    '''ENTITY STUFF'''
    def add_entity_to_db(type: str, name, desc, value, num_owned, auto_update, stock_symbol, id):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            add_asset_query = ("INSERT INTO asset (entity_value, entity_amount, entity_name, entity_desc, entity_auto_update, entity_stock_symbol, id) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            
            add_liability_query = ("INSERT INTO liability (entity_value, entity_amount, entity_name, entity_desc, entity_auto_update, entity_stock_symbol, id) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            
            new_entity_data = (value, num_owned, name, desc, auto_update, stock_symbol, id)

            if type == "asset":
                #add the data to database using the above query
                db_cursor.execute(add_asset_query, new_entity_data) #execute() sends query to the SQL database server for execution
            else: #type == "liability"
                db_cursor.execute(add_liability_query, new_entity_data)

            db.commit() #commit() saves changes, made by cursor(), into the database

            #close database connection; avoid any possible trouble because we good programmer
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not store income to database. Error: {e}")
            return False #added bools for testing
        return True
    
    def pull_entities_from_database(entity_portfolio: EntityPortfolio):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()
            db_cursor.execute("SELECT * FROM asset")
            assets = db_cursor.fetchall()
            for row in assets:
                value = row[0]
                amount = row[1]
                name = row[2]
                desc = row[3]
                auto_update = row[4]
                stock_symbol = row[5]
                the_id = row[6]

                #add transaction to the transaction_list
                asset = Entity.Entity(value, amount, name, desc, auto_update, stock_symbol)
                asset.set_entity_id(the_id)
                entity_portfolio.add_asset(asset, True)
                

            '''Liabilities'''
            db_cursor.execute("SELECT * FROM liability")
            liabilities = db_cursor.fetchall()
            for row in liabilities:
                value = row[0]
                amount = row[1]
                name = row[2]
                desc = row[3]
                auto_update = row[4]
                stock_symbol = row[5]
                the_id = row[6]

                #add transaction to the transaction_list
                liability = Entity.Entity(value, amount, name, desc, auto_update, stock_symbol) #this line is where it fails
                liability.set_entity_id(the_id)
                entity_portfolio.add_liability(liability, True)
            
            #close database connection
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not grab income to database Please exit AdvFi and fix to save your data. Error: {e}")
            return False #added bools for testing
        return True
    

    def delete_entity_from_db(entity_portfolio: EntityPortfolio, type: str, id):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            del_asset_query = ("DELETE FROM asset WHERE id = %s")
            del_liability_query = ("DELETE FROM liability WHERE id = %s")

            if type == "asset":
                #add the data to database using the above query
                db_cursor.execute(del_asset_query, (id,)) #execute() sends query to the SQL database server for execution
            else: #type == "liability"
                db_cursor.execute(del_liability_query, (id,)) #passing 'id' as a 'tuple' to make .execute() func happy

            db.commit() #commit() saves changes, made by cursor(), into the database

            #close database connection; avoid any possible trouble because we good programmer
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not remove entity from database. Error: {e}")
            return False #added bools for testing
        return True


    #ENTITY EDIT METHODS
    def edit_entity_name(entity_id: str, type: str, new_name: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            update_query = f"UPDATE {type} SET entity_name = %s WHERE id = %s"
            db_cursor.execute(update_query, (new_name, entity_id))

            db.commit()
            print(f"Entity name updated to '{new_name}' for ID {entity_id}.")
            db_cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Could not update entity name. Error: {e}")
            return False

    def edit_entity_description(entity_id: str, type: str, new_description: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            update_query = f"UPDATE {type} SET entity_desc = %s WHERE id = %s"
            db_cursor.execute(update_query, (new_description, entity_id))

            db.commit()
            print(f"Entity description updated for ID {entity_id}.")
            db_cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Could not update entity description. Error: {e}")
            return False


    def edit_entity_amount(entity_id: str, type: str, new_amount: int):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            update_query = f"UPDATE {type} SET entity_amount = %s WHERE id = %s"
            db_cursor.execute(update_query, (new_amount, entity_id))

            db.commit()
            print(f"Entity amount updated to '{new_amount}' for ID {entity_id}.")
            db_cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Could not update entity amount. Error: {e}")
            return False


    def edit_entity_value(entity_id: str, type: str, new_value: float):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            update_query = f"UPDATE {type} SET entity_value = %s WHERE id = %s"
            db_cursor.execute(update_query, (new_value, entity_id))

            db.commit()
            print(f"Entity value updated to '{new_value}' for ID {entity_id}.")
            db_cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Could not update entity value. Error: {e}")
            return False



    '''Category stuff!'''
    def add_category(cat_name: str, cat_desc: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            add_cat_query = ("INSERT INTO category (cat_name, cat_desc) " "VALUES (%s, %s)")
            
            new_entity_data = (cat_name, cat_desc)
            db_cursor.execute(add_cat_query, new_entity_data)
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add category to the database. Error: {e}")
            return False #added bools for testing
        return True
    
    #budget is part of category
    def update_budget(cat_name: str, new_budget: float):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database

            update_query = "UPDATE category SET budget = %s WHERE cat_name = %s"
            db_cursor.execute(update_query, (new_budget, cat_name))
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add category to the database. Error: {e}")
            return False #added bools for testing
        return True
    
    #budget is part of category
    def delete_budget(cat_name: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database

            new_budget = -1.0 #-1.0 means no budget
            
            update_query = "UPDATE category SET budget = %s WHERE cat_name = %s"
            db_cursor.execute(update_query, (new_budget, cat_name))
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add category to the database. Error: {e}")
            return False #added bools for testing
        return True
    

    def set_transaction_category(transaction_list: TransactionList, id: str, type: str, category_name: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            update_income_query = ("UPDATE income SET category_name = %s WHERE id = %s")
            
            update_expense_query = ("UPDATE expense SET category_name = %s WHERE id = %s")
            
            new_trans_data = (category_name, id)
            if type == "income":
                db_cursor.execute(update_income_query, new_trans_data)
            else:
                db_cursor.execute(update_expense_query, new_trans_data)
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not set transaction category to the database. Error: {e}")
            return False #added bools for testing
        return True

    def set_entity_category(entity_portfolio: EntityPortfolio, id: str, type: str, category_name: str):
        MainUI.MainUI.utility_print(f"Type: {type}, ID: {id}, Category: {category_name}")
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            update_asset_query = ("UPDATE asset SET cat_name = %s WHERE id = %s")
            update_liability_query = ("UPDATE liability SET cat_name = %s WHERE id = %s")

            MainUI.MainUI.utility_print(f"Type: {type}, ID: {id}, Category: {category_name}")
            
            new_trans_data = (category_name, id)
            if type == "asset":
                db_cursor.execute(update_asset_query, new_trans_data)
            else:
                db_cursor.execute(update_liability_query, new_trans_data)
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not set transaction category to the database. Error: {e}")
            return False #added bools for testing
        return True

    def pull_categories_from_db(cat_list: CategoryList):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            db_cursor.execute("SELECT * FROM category")
            categories = db_cursor.fetchall()
            for row in categories:
                name = row[0]
                desc = row[1]
                income_count = row[2]
                expense_count = row[3]
                asset_count = row[4]
                liability_count = row[5]
                temp_cat = Category.Category(name, desc)
                temp_cat.set_income(income_count)
                temp_cat.set_expense(expense_count)
                temp_cat.set_asset(asset_count)
                temp_cat.set_liability(liability_count)
                cat_list.add_category(temp_cat)

            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add category to the database. Error: {e}")
            return False #added bools for testing
        return True
    
    def update_category_counts(cat_name: str, income_count: int, type: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            update_income_query = ("UPDATE category SET income_count = %s WHERE cat_name = %s")
            update_expense_query = ("UPDATE category SET expense_count = %s WHERE cat_name = %s")
            update_asset_query = ("UPDATE category SET asset_count = %s WHERE cat_name = %s")
            update_liability_query = ("UPDATE category SET liability_count = %s WHERE cat_name = %s")
            
            new_trans_data = (income_count, cat_name)
            if type == "income":
                db_cursor.execute(update_income_query, new_trans_data)
            elif type == "expense":
                db_cursor.execute(update_expense_query, new_trans_data)
            elif type == "asset":
                db_cursor.execute(update_asset_query, new_trans_data)
            else: #type == "liability"
                db_cursor.execute(update_liability_query, new_trans_data)
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not set transaction category to the database. Error: {e}")
            return False #added bools for testing
        return True
    




    #REPORT METHODS!!!!
    def add_income_report(report_str: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            # Add report to income_report table
            add_report_query = ("INSERT INTO income_report (income_entries_string) "  "VALUES (%s)")
            db_cursor.execute(add_report_query, (report_str,))

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return True

    def get_income_report():
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            # Add report to income_report table
            query = ("SELECT * FROM income_report WHERE id = %s")
            #the_report = db_cursor.execute(query, (report_id,))
            db_cursor.execute("SELECT * FROM income_report")
            the_report = db_cursor.fetchall()

            for row in the_report:
                MainUI.MainUI.utility_print(row)

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return True


    def add_spending_report(report_str: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            # Add report to income_report table
            add_report_query = ("INSERT INTO spending_report (income_entries_string) "  "VALUES (%s)")
            db_cursor.execute(add_report_query, (report_str,))

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return True

    def get_spending_report():
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            # Add report to income_report table
            db_cursor.execute("SELECT * FROM spending_report")
            the_report = db_cursor.fetchall()

            #MainUI.MainUI.utility_print(the_report)
            for row in the_report:
                MainUI.MainUI.utility_print(row)

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return True
    

    def add_health_report(report_str: str):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            # Add report to income_report table
            add_report_query = ("INSERT INTO health_report (income_entries_string) "  "VALUES (%s)")
            db_cursor.execute(add_report_query, (report_str,))

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return True

    def get_health_report():
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            # Add report to income_report table
            db_cursor.execute("SELECT * FROM health_report")
            the_report = db_cursor.fetchall()

           # MainUI.MainUI.utility_print(the_report[1])
            for row in the_report:
                MainUI.MainUI.utility_print(row)

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return True
    


    # USER ACCOUNT QUERIES
    def create_user_account(user_account: UserAccount):
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            # Add report to income_report table
            #db_cursor.execute("INSERT INTO health_report (income_entries_string) "  "VALUES (%s)", )
            #the_report = db_cursor.fetchall()

            user_data = (user_account._password, user_account._pin)
            query = ("INSERT INTO the_user (password, pin) "  "VALUES (%s, %s)")
            db_cursor.execute(query, user_data)

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return True
    
    def get_user_account():
        empty_account = UserAccount.UserAccount()
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            # Add report to income_report table
            #db_cursor.execute("INSERT INTO health_report (income_entries_string) "  "VALUES (%s)", )
            #the_report = db_cursor.fetchall()

            query = ("SELECT * FROM the_user")
            result = db_cursor.execute(query)

            user_account = UserAccount.UserAccount()
            user_account.set_password(result[0])
            user_account.set_pin(result[1])



            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return empty_account
        return user_account
    
    def check_account_state():
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            query = ("SELECT * FROM user_state")
            db_cursor.execute(query)
            the_state = db_cursor.fetchone()
            the_state = the_state[0]

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
            return the_state
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return the_state
    
    def set_account_state():
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            update_query = ("UPDATE user_state SET user_exists = TRUE")
            db_cursor.execute(update_query)

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return True
    
    def delete_account():
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor()

            #drop tables
            db_cursor.execute("drop table the_user")
            db_cursor.execute("drop table user_state")

            #recreate tables
            db_cursor.execute("CREATE TABLE the_user (password VARCHAR(255) NOT NULL,pin INT)")
            db_cursor.execute("CREATE TABLE user_state (user_exists BOOLEAN DEFAULT FALSE)")
            db_cursor.execute("INSERT INTO user_state () VALUES ()")

            # Commit changes
            db.commit()
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not add report to the database. Error: {e}")
            return False
        return True