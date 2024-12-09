'''
this file defines a class FinancialHealthReport, which is used to assess the financial health of the user
by Jaden Winterpacht
'''

import EntityPortfolio
from datetime import date
from Report import Report
import TransactionList
import Transaction
import Entity
import Controller
import MainUI

class FinancialHealthReport(Report):
    def __init__(self, report_date: date, transaction_list: TransactionList, entity_portfolio: EntityPortfolio):
        super().__init__(report_date)
        self._net_worth = self.calculate_current_net_worth(entity_portfolio, transaction_list)
        self._total_assets = entity_portfolio.get_assets_value()
        self._total_liabilities = entity_portfolio.get_liabilities_value()
        self._total_income = transaction_list.get_total_income()
        self._total_expenses = transaction_list.get_total_expenses()
        self._savings_rate = self.calculate_savings_rate()
        self._asset_to_debt_ratio = self.calculate_asset_to_debt_ratio(entity_portfolio, transaction_list)
        self._investment_return = self.calculate_investment_return(entity_portfolio)
        self._advfi_score = self.calculate_advfi_score()

    def calculate_savings_rate(self) -> float:
        '''
        calculates the percent of income that the user is saving

        :return: the savings rate
        '''
        net_income = self._total_income - self._total_expenses
        savings_rate = (net_income / self._total_income) * 100
        return savings_rate
    
    def calculate_investment_return(self, entity_portfolio: EntityPortfolio):
        #set variables
        if entity_portfolio.get_asset_list() == []:
            return -1
        initial_investment_value = 0
        current_investment_value = 0
        asset_list = entity_portfolio.get_asset_list()
        for asset in asset_list:
            initial_investment_value += (asset._initial_value * asset.get_amount())
            current_investment_value += (asset.get_total_value())
        investment_return = ((current_investment_value - initial_investment_value) / initial_investment_value) * 100
        return investment_return

    def calculate_asset_to_debt_ratio(self, entity_portfolio: EntityPortfolio, transaction_list: TransactionList):
        '''
        the asset-to-debt ratio is calculated by adding total asset value and total income, subtracting expenses,
        and then dividing it all by total debt.
        this will not be displayed to the user but used in the calculation of the AdvFi Financial Health Score.

        :return: the asset-to-debt ratio
        '''
        total_assets = entity_portfolio.get_assets_value()
        total_income = transaction_list.get_total_income()
        total_expenses = transaction_list.get_total_expenses()
        total_debt = entity_portfolio.get_liabilities_value()
        # if user has no debt, double their AdvFi Score
        if total_debt == 0:
            return 2

        asset_to_debt_ratio = ((total_assets + total_income - total_expenses) / total_debt) * 100
        return asset_to_debt_ratio
    
    def calculate_current_net_worth(self, entity_portfolio: EntityPortfolio, transaction_list: TransactionList):
        entity_portfolio.update_values()
        net_worth = 0
        net_worth += transaction_list.get_total_income()
        net_worth -= transaction_list.get_total_expenses()
        net_worth += entity_portfolio.total_value
        return net_worth
    
    def calculate_advfi_score(self):
        advfi_score = abs(int(self._savings_rate * self._investment_return * self._asset_to_debt_ratio))
        return advfi_score
    
    def generate_report(self):
        header = f"Financial Health Report\n{self._report_date}\n---------------------------\n"
        net_worth = f"Net worth: ${self._net_worth}\n\n"
        items = f"Total asset value: ${self._total_assets}\nTotal debt value: ${self._total_liabilities}\nTotal income: ${self._total_income}\nTotal spending: ${self._total_expenses}\n\n"
        savings_rate = f"Savings rate: {self._savings_rate:.2f}%\n"
        inv_return = self._investment_return
        if inv_return != -1:
            investment_return = f"Investment return: {self._investment_return}%\n\n"
        else:
            investment_return = f"Investment return: N/A\n\n"
        advfi_score = f"AdvFi Score: {self._advfi_score}\n"
        financial_health_report = header + net_worth + items + savings_rate + investment_return + advfi_score
        MainUI.MainUI.utility_print(financial_health_report)

    def to_string(self) -> str:
        header = f"Financial Health Report\n{self._report_date}\n---------------------------\n"
        net_worth = f"Net worth: ${self._net_worth}\n\n"
        items = f"Total asset value: ${self._total_assets}\nTotal debt value: ${self._total_liabilities}\nTotal income: ${self._total_income}\nTotal spending: ${self._total_expenses}\n\n"
        savings_rate = f"Savings rate: {self._savings_rate:.2f}%\n"
        inv_return = self._investment_return
        if inv_return != -1:
            investment_return = f"Investment return: {self._investment_return}%\n\n"
        else:
            investment_return = f"Investment return: N/A\n\n"
        advfi_score = f"AdvFi Score: {self._advfi_score}\n"
        financial_health_report = header + net_worth + items + savings_rate + investment_return + advfi_score
        return financial_health_report
    
    def get_header(self) -> str:
        header = f"Financial Health Report\n{self._report_date}"
        return header
    
    def get_body(self) -> str:
        body = ""
        net_worth = f"Net worth: ${self._net_worth}\n\n"
        items = f"Total asset value: ${self._total_assets}\nTotal debt value: ${self._total_liabilities}\nTotal income: ${self._total_income}\nTotal spending: ${self._total_expenses}\n\n"
        savings_rate = f"Savings rate: {self._savings_rate:.2f}%\n"
        inv_return = self._investment_return
        if inv_return != -1:
            investment_return = f"Investment return: {self._investment_return}%\n\n"
        else:
            investment_return = f"Investment return: N/A\n\n"
        body = net_worth + items + savings_rate + investment_return
        return body
    
    def get_score(self) -> str:
        return f"AdvFi Score: {self._advfi_score}"
