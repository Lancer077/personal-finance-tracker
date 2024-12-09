import csv
import MainUI 
import Transaction
from datetime import date, datetime as dt
import TransactionList
import Entity
import EntityPortfolio
import UserAccount
import Category
import CategoryList
import mysql.connector #allows Python to talk to MySQL database
import MySQLOperations
import ReportFactory
import IncomeReport
import SpendingReport
import FinancialHealthReport
import Report
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

report_factory = ReportFactory.ReportFactory()

class Operations:
    
    
    def create_user_account_operations(account: UserAccount, password: str, pin: str):
        account.new_user = False
        account.set_password(password)
        account.set_pin(pin)
        

    def create_and_add_transaction(transaction_list: TransactionList, amount, date, desc, type: str):
        amount = float(amount)

        # Do this only if it is a string
        if isinstance(date,str):
            date = dt.strptime(date, '%m/%d/%y')

        transaction = Transaction.Transaction(amount, date, desc)

        if type == "income":
            transaction_list.add_income_transaction(transaction, False) #make sure that it updates local list, not just DB
            #Now, store the income transaction into the database
            MySQLOperations.MySQLOperations.add_transaction_to_database(transaction, "income")
        elif type == "expense":
            transaction_list.add_expense_transaction(transaction, False)
            MySQLOperations.MySQLOperations.add_transaction_to_database(transaction, "expense")
        
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
            #add to categorization to the income in the database
            MySQLOperations.MySQLOperations.set_transaction_category(transaction_list, transaction_id, type, category_name)
        elif type == "expense":
            category.add_expense(transaction)
            MySQLOperations.MySQLOperations.set_transaction_category(transaction_list, transaction_id, type, category_name)
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
            #add categorization of entity to DATABASE!!
            MySQLOperations.MySQLOperations.set_entity_category(entity_list, entity_id, type, category_name)
        elif type == "liability":
            category.add_liability(entity)
            MySQLOperations.MySQLOperations.set_entity_category(entity_list, entity_id, type, category_name)
        entity.set_category_name(category_name)

    def get_entity(entity_portfolio: EntityPortfolio, type: str, id: str) -> Entity:
        if type == "asset":
            return entity_portfolio.get_entity(id)
        elif type == "liability":
            return entity_portfolio.get_entity(id)
        


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
            entity_portfolio.add_asset(new_entity, False)
        elif type == "liability":
            entity_portfolio.add_liability(new_entity, False)
            
        MainUI.MainUI.add_entity_success(type)



    def remove_entity_from_portfolio(entity_portfolio, type, entity_id):
        #since we have already checked to make sure that the entity id is in the respective list,
        #we do not need to worry about that
        entity_id = int(entity_id)

        if entity_id == -1:
            MainUI.MainUI.action_cancelled()
            return

        if type == "asset":
            MySQLOperations.MySQLOperations.delete_entity_from_db(entity_portfolio, "asset", entity_id)
            entity_portfolio.remove_asset(entity_id)

        elif type == "liability":
            MySQLOperations.MySQLOperations.delete_entity_from_db(entity_portfolio, "liability", entity_id)
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
        MySQLOperations.MySQLOperations.add_category(new_cat_name, new_cat_desc)
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
    
    def spending_management_menu_import_spending_CSV_operations(fileName: str, transaction_list: TransactionList):

        with open(fileName, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row

            for row in csv_reader:
                if len(row) < 5:  # Ensure there are enough columns
                    continue

                # Parse transaction date
                try:
                    transaction_date = dt.strptime(row[0], '%m/%d/%Y')
                except ValueError:
                    print(f"Invalid date format in row: {row}")
                    continue

                # Determine amount and description
                withdrawal_amount = row[3].strip()
                deposit_amount = row[4].strip()
                description = row[2].strip() if row[2] else "No description"

                # Determine income or expense and parse amount
                if withdrawal_amount:
                    amount = abs(float(withdrawal_amount))
                    income_or_expense = "Expense"
                elif deposit_amount:
                    amount = float(deposit_amount)
                    income_or_expense = "Income"
                else:
                    print(f"Invalid transaction data in row: {row}")
                    continue

                # Add transaction to the correct list
                if income_or_expense == "Expense":
                    Operations.create_and_add_transaction(transaction_list, amount=amount, date=transaction_date, desc=description, type="expense")
                else:
                    Operations.create_and_add_transaction(transaction_list, amount=amount, date=transaction_date, desc=description, type="income")
        
        
    def print_transactions(transaction_list:TransactionList) -> str:
        transactions = transaction_list.print_transactions()
        return transactions


    def print_income_list(transaction_list):
        return transaction_list.print_incomes()

    def print_expense_list(transaction_list):
        return transaction_list.print_expenses()
    
    '''
    WARNING: This function will CRASH the program if you're not on at least: mysql-connector version 2.2.9
    Run in bash: pip install --upgrade mysql-connector-python
    '''
    def add_income_to_database(income_transaction: Transaction):
        #Validator.validate_database_connection() proves that db connection is established. But, keep try-catch in case of unforseen failure?
        try:
            db = mysql.connector.connect(user='advfi_user', password='advfi_password', host='localhost', database='advfi_database')
            db_cursor = db.cursor() #cursor() acts as an interace between AdvFi and the database
            add_income_query = ("INSERT INTO income (amount, transaction_date, trans_desc, category_name, id) "
                            "VALUES (%s, %s, %s, %s, %s)") # '%s' is a SQL.connector placeholder for ANY datatype...so we WIN!
            
            new_income_data = (income_transaction.get_amount(), income_transaction.get_transaction_date(),
                            income_transaction.get_description(), income_transaction.get_category_name(), income_transaction.get_transaction_id() )

            #add the data to database using the above query
            db_cursor.execute(add_income_query, new_income_data) #execute() sends query to the SQL database server for execution
            db.commit() #commit() saves changes, made by cursor(), into the database

            #close database connection; avoid any possible trouble because we good programmer
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not store income to database. Error: {e}")
            return False #added bools for testing
        return True

    def pull_incomes_from_database(transaction_list: TransactionList):
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
                transaction_list.add_income_transaction(trans)

            #close database connection
            db_cursor.close()
            db.close()
        except Exception as e:
            print(f"Could not grab income to database Please exit AdvFi and fix to save your data. Error: {e}")
            return False #added bools for testing
        return True
    
    def financial_reports_menu_report_operations(report_type, transaction_list: TransactionList, entity_portfolio=None) -> Report:
        if report_type == "financial health":
            report = report_factory.get_report(report_type, transaction_list, entity_portfolio)
        # income or spending report
        else:
            report = report_factory.get_report(report_type, transaction_list)
        return report

    # We can use validate_file_name to validate input 
    def generate_pdf_report(filename: str, reportTyp: str, reportStr: str, reportScr = ""):
        logo = r"""
            _      __                     ____  _____ 
           / \    |  \   \     /         |        |   
          /---\   |   |   \   /    ===   |--      |   
         /     \  |__/     \_/           |      __|__ 
        """
        filename += ".pdf"
            # Create a new PDF
        c = canvas.Canvas(filename)
        
        # Set font and size for the logo
        c.setFont("Courier-Bold", 12)
        
        # Draw the logo text
        y_position = 750  # Start drawing at this y-coordinate
        x_position = 100
        for line in logo.splitlines():
            c.drawString(100, y_position, line)
            y_position -= 15  # Move down by 15 units for the next line

        # Set font for the "Income Report" title text
        c.setFont("Helvetica-Bold", 16)
        lines = reportTyp.split('\n')
        title_width = c.stringWidth(lines[0], "Helvetica-Bold", 16)
        x_position = (c._pagesize[0] - title_width) / 2  # Center the text on the page

        # Calculate the width of the "Income Report" text
        report_title = lines[0]
        report_date = lines[1]
        y_position -= 30
        c.drawString(x_position, y_position, report_title)
        y_position -= 30
        c.drawString(x_position, y_position, report_date)
        y_position -= 60

        # Calculate the x position to center the title text

        # Draw the "Income Report" text centered
        #c.drawString(x_position, y_position - 30, lines[0])  # Position it below the logo

        # Set font for the "Report" text (left justified)
        c.setFont("Helvetica", 12)
        x_position = 0
        # Draw the "Report" text below and left justified
        lines = reportStr.split('\n')
        for line in lines:
            items = line.split('\t')
            x_position = 0
            for item in items:
                x_position += 110
                c.drawString(x_position, y_position, item)
            y_position-=15
        
        #c.drawString(100, y_position - 60, reportStr)  # Left-justified at the same x as the logo

        if reportScr != "":
            reportScr = str(reportScr)
            c.setFont("Helvetica-Bold", 40)

            # Calculate the width of the score text for medium alignment
            score_width = c.stringWidth(reportScr, "Helvetica-Bold", 40)
            medium_x_position = (c._pagesize[0] - score_width) / 2

            # Add margin above the score
            margin_above_score = 20  # Adjust this value to change the margin size
            adjusted_y_position = y_position - 90 - margin_above_score

            # Draw the ADV-FI score text with adjusted position
            c.drawString(medium_x_position, adjusted_y_position, reportScr)

            # Save the PDF
        c.save()
        print(f"PDF saved as {filename}")