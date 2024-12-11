import pytest
import Category
import CategoryList
import Transaction
import TransactionList
from datetime import datetime, timedelta
import EntityPortfolio
import Entity
import Controller

'''
Test cases for use case 3.1.4 "Create new categories for spending and expenses"
'''
@pytest.fixture
def category_list():
    return CategoryList.CategoryList()

@pytest.fixture
def sample_category():
    def create_category(name, description=""):
        return Category.Category(name, description)
    return create_category

def test_add_category_normal(category_list, sample_category):
    category = sample_category("Groceries", "Food and household supplies")
    category_list.add_category(category)
    assert category.get_name() in category_list.get_category_names()
    assert category_list.get_category_count() == 1
    assert category.get_description() == "Food and household supplies"

# allow users to enter blank categories
def test_add_category_blank(category_list, sample_category):
    category = sample_category("", "")
    category_list.add_category(category)
    assert category.get_name() in category_list.get_category_names()
    assert category_list.get_category_count() == 1
    assert category.get_description() == ""

def test_add_category_numbers(category_list):
    with pytest.raises(TypeError):
        category = Category(123, 456)
        category_list.add_category(category)

'''
Test cases for use case 3.1.15 "Create spending events"
'''
@pytest.fixture
def transaction_list():
    return TransactionList.TransactionList()

@pytest.fixture
def sample_transaction():
    def create_transaction(amount, days_ago, description=""):
        transaction_date = datetime.now() - timedelta(days=days_ago)
        return Transaction.Transaction(amount, transaction_date, description)
    return create_transaction

def test_add_spending_event(transaction_list, sample_transaction):
    expense = sample_transaction(22.22, 1, "Jewel trip")
    transaction_list.add_expense_transaction(expense, database_reading=False)
    
    assert transaction_list.get_total_expenses() == 22.22
    assert transaction_list.get_transaction_count() == 1
    assert transaction_list.is_transaction_in_list(expense.get_transaction_id(), "expense") is True

def test_add_multiple_spending_events(transaction_list, sample_transaction):
    expense1 = sample_transaction(40.56, 1, "Movie theater")
    expense2 = sample_transaction(14.07, 2, "Starbucks")
    
    transaction_list.add_expense_transaction(expense1, database_reading=False)
    transaction_list.add_expense_transaction(expense2, database_reading=False)
    
    assert transaction_list.get_total_expenses() == 54.63
    assert transaction_list.get_transaction_count() == 2
    assert transaction_list.is_transaction_in_list(expense1.get_transaction_id(), "expense") is True
    assert transaction_list.is_transaction_in_list(expense2.get_transaction_id(), "expense") is True

'''
Test cases for use case 3.1.6 "Calculate net worth"
'''
@pytest.fixture
def entity_portfolio():
    return EntityPortfolio.EntityPortfolio()

@pytest.fixture
def sample_entity():
    def create_entity(value, amount, name, description, auto_update, stock_symbol=""):
        return Entity.Entity(value, amount, name, description, auto_update, stock_symbol)
    return create_entity

def test_calculate_net_worth():
    entity1 = Entity.Entity(200, 4, "Brick", "Used to build houses", False, "BRCK")
    entity2 = Entity.Entity(2000, 4, "Apple stock", "", False, "AAPL")

    entity_portfolio = EntityPortfolio.EntityPortfolio()

    entity_portfolio.add_asset(entity1, False)
    entity_portfolio.add_asset(entity2, False)
    
    net_worth = 0
    net_worth += entity_portfolio.total_value

    assert net_worth == 8800
