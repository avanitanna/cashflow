import math
import sys
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama
from prompts import *
from input_wrappers import InputOutput, ConsoleInput

class OpportunityDecision(BaseModel):
    yes_or_no: bool = Field(description="whether you should buy or sell this opportunity")
    reasoning: str = Field(description="reasoning behind the recommendation")

class DealSizeDecision(BaseModel):
    big: bool = Field(description="whether you should choose a big deal")
    reasoning: str = Field(description="reasoning behind the recommendation")

class CharityDecision(BaseModel):
    yes_or_no: bool = Field(description="whether you should donate to charity")
    reasoning: str = Field(description="reasoning behind the recommendation")

class BorrowRepayDecision(BaseModel):
    borrow_repay: str = Field(description="whether you should borrow or repay or neither")
    amount: Optional[int] = Field(description="the amount to borrow/repay (must be multiple of 1000, 0 if neither)", default=0)
    reasoning: str = Field(description="reasoning behind the recommendation")

class Asset:
    def __init__(self, cost, cashflow):
        self.cost = cost
        self.cashflow = cashflow

class Liability:
    def __init__(self, cost, expense):
        self.cost = cost
        self.expense = expense

class CashflowGame:
    def __init__(self, llm: BaseChatModel, inp: InputOutput):
        self.llm = llm
        self.financial_statement = {
            'cash': 0,
            'income': 0,
            'expenses': 0,
            'assets': {}, # Using dict with IDs as keys
            'liabilities': {} # Using dict with IDs as keys
        }
        self.next_asset_id = 0
        self.next_liability_id = 1
        self.inp = inp

    def financials_to_string(self):
        output = []

        # Basic financial info
        output.append(f"Cash: ${self.financial_statement['cash']}")
        output.append(f"Income: ${self.financial_statement['income']}")
        output.append(f"Expenses: ${self.financial_statement['expenses']}")

        # Assets section
        output.append("\nAssets:")
        for asset_id, asset in self.financial_statement['assets'].items():
            output.append(f"  ID {asset_id}:")
            output.append(f"    Cost: ${asset.cost}")
            output.append(f"    Cashflow: ${asset.cashflow}")

        # Liabilities section
        output.append("\nLiabilities:")
        for liability_id, liability in self.financial_statement['liabilities'].items():
            output.append(f"  ID {liability_id}:")
            output.append(f"    Cost: ${liability.cost}")
            output.append(f"    Expense: ${liability.expense}")

        return "\n".join(output) 

    def convert_to_int(self, value):
        try:
            return int(value)
        except ValueError:
            return ''

    def opportunity(self):
        # Get all opportunity info from input wrapper
        opp_info = self.inp.get_opportunity()
        choice = opp_info.get("choice")
        buy_sell = opp_info.get("buy_sell")
        asset_id = opp_info.get("asset_id")
        cost = opp_info.get("cost")
        downpayment = opp_info.get("downpayment")
        cashflow = opp_info.get("cashflow")
        lower_trading_range = opp_info.get("lower_trading_range")
        upper_trading_range = opp_info.get("upper_trading_range")
        buyer_offer = opp_info.get("buyer_offer")
        self.inp.output_financials(self.financial_statement)
        #roi = (cashflow*12/downpayment) * 100 if isinstance(cashflow, int) and isinstance(downpayment, int) else ''
        roi = ''
        if isinstance(cashflow, int) and isinstance(downpayment, int):
            if downpayment > 0:
                roi = f"{(cashflow*12/downpayment) * 100:.2f}%"
            elif cashflow > 0:  # If there's positive cashflow with no downpayment
                roi = "Infinite%"  
            else:
                roi = "0%"

        prompt_template = ChatPromptTemplate([("user", opportunity_prompt)])
        prompt = prompt_template.invoke({
            "buy_sell": buy_sell,
            "cost": cost,
            "downpayment": downpayment,
            "cashflow": cashflow,
            "roi": str(roi) + "%",
            "lower_trading_range": lower_trading_range,
            "upper_trading_range": upper_trading_range,
            "buyer_offer": buyer_offer,
            "financial_statement": self.financials_to_string()
            })

        # LLM evaluates the opportunity
        recommendation = self.evaluate(prompt, OpportunityDecision)
        self.inp.print_deal_rec(recommendation)
        if recommendation.yes_or_no:
            res = {}
            if buy_sell == 'buy':
                if self.financial_statement['cash'] >= downpayment:
                    res['cash'] = -downpayment
                else:
                    self.inp.note_loan()
                    loan_amount = math.ceil((downpayment - self.financial_statement['cash'])/1000)*1000
                    res['cash'] = -downpayment+loan_amount
                    res['liabilities'] = {
                        "operation": "update",
                        "id": 0,
                        "cost": loan_amount,
                        "expense": 0.1*loan_amount
                    }
                res['assets'] = {
                    "operation": "add",
                    "cost": cost,
                    "cashflow": cashflow
                }
            else:
                res['cash'] = cost
                res['assets'] = {
                    "operation": "remove",
                    "id": asset_id
                }
            self.update_financials(res)

        return

    def deal(self):
        # Get LLM recommendation for deal size
        prompt_template = ChatPromptTemplate([("user", deal_size_prompt)])
        prompt = prompt_template.invoke({'financial_statement': self.financials_to_string()})
        deal_recommendation = self.evaluate(prompt=prompt, result_schema=DealSizeDecision)
        self.inp.print_deal_size_rec(deal_recommendation)

        # Get deal details and evaluate
        self.opportunity()
        return

    def no_deal(self):
        # payday, downsized, baby, doodads
        no_deal_info = self.inp.get_no_deal()
        cost = no_deal_info.get("cost")
        baby = no_deal_info.get("baby")
        res = {}
        if baby == "yes":
            res = {
                    "liabilities": {
                        "operation": "add",
                        "cost": 0,
                        "expense": cost
                    }
            }
        else:
            if cost > self.financial_statement['cash']:
                self.inp.note_loan()
                loan_amount = math.ceil((cost - self.financial_statement['cash'])/1000)*1000
                res = {
                    "cash": -cost+loan_amount,
                    "liabilities": {
                        "operation": "update",
                        "id": 0,
                        "cost": loan_amount,
                        "expense": 0.1*loan_amount
                    }
                }
            else:
                res = {
                    "cash": -cost
                }
        self.update_financials(res)

    def charity(self):

        prompt_template = ChatPromptTemplate([("user", charity_prompt)])
        prompt = prompt_template.invoke({'financial_statement': self.financials_to_string()})
        charity_recommendation = self.evaluate(prompt=prompt, result_schema=CharityDecision)
        self.inp.print_charity_rec(charity_recommendation)

        # you can only donate if you have the money to do so
        if charity_recommendation.yes_or_no:
            res = {
                "cash": -0.1*self.financial_statement['income']
            }
            self.update_financials(res)
        return

    def evaluate(self, prompt, result_schema):
        recommendation = None
        messages = prompt.to_messages()
        messages = [SystemMessage(content=system_prompt)] + messages
        for message in messages:
            self.inp.print_message(message)
        # Send to LLM for evaluation
        while True:
            try:
                response = self.llm.invoke(messages)
                self.inp.print_message(response)
            except Exception as e:
                print(e)
                sys.exit(1)
            break
        while True:
            try:
                llm_with_structured_output = self.llm.with_structured_output(result_schema)
                result_prompt_message = HumanMessage(content=result_prompt)
                recommendation = llm_with_structured_output.invoke(messages + [response, result_prompt_message])
            except Exception as e:
                print(e)
                sys.exit(1)
            break
        return recommendation

    def repay_borrow(self):
        prompt_template = ChatPromptTemplate([("user", repay_borrow_prompt)])
        prompt = prompt_template.invoke({'financial_statement': self.financials_to_string()})
        # Get LLM recommendation for borrowing/repayment amount and decision
        borrow_repay_recommendation = self.evaluate(prompt=prompt, result_schema=BorrowRepayDecision)
        self.inp.print_borrow_repay_rec(borrow_repay_recommendation)

        # Update financial statement based on LLM recommendations
        if borrow_repay_recommendation.borrow_repay == 'borrow':
            res = {
                "cash": borrow_repay_recommendation.amount,
                "liabilities": {
                    "operation": "update",
                    "id": 0,
                    "cost": borrow_repay_recommendation.amount,
                    "expense": 0.1*borrow_repay_recommendation.amount
                }
            }
            self.update_financials(res)
        elif borrow_repay_recommendation.borrow_repay == 'repay':
            res = {
                "cash": -borrow_repay_recommendation.amount,
                "liabilities": {
                    "operation": "update",
                    "id": 0,
                    "cost": -borrow_repay_recommendation.amount,
                    "expense": -0.1*borrow_repay_recommendation.amount
                }
            }
            self.update_financials(res)
        return 

    def update_financials(self, res):
        # Update financial statement based on LLM recommendations
        self.financial_statement['cash'] += res.get('cash', 0)
        self.financial_statement['income'] += res.get('income', 0)
        self.financial_statement['expenses'] += res.get('expenses', 0)

        # Handle asset changes
        if 'assets' in res:
            # Check if assets is a dictionary and convert to list for uniform handling
            assets_list = [res['assets']] if isinstance(res['assets'], dict) else res.get('assets', [])
            for asset in assets_list:
                if asset['operation'] == 'add':
                    asset_id = self.next_asset_id
                    self.financial_statement['assets'][asset_id] = Asset(
                        asset['cost'],
                        asset['cashflow']
                    )
                    self.financial_statement['income'] += asset['cashflow']
                    self.next_asset_id += 1
                elif asset['operation'] == 'remove':
                    asset_id = asset['id']
                    if asset_id in self.financial_statement['assets']:
                        removed_asset = self.financial_statement['assets'][asset_id]
                        self.financial_statement['income'] -= removed_asset.cashflow
                        del self.financial_statement['assets'][asset_id]

        # Handle liability changes
        if 'liabilities' in res:
            # Check if liabilities is a dictionary and convert to list for uniform handling
            liabilities_list = [res['liabilities']] if isinstance(res['liabilities'], dict) else res.get('liabilities', [])
            for liability in liabilities_list:
                if liability['operation'] == 'add':
                    liability_id = self.next_liability_id
                    self.financial_statement['liabilities'][liability_id] = Liability(
                        liability['cost'],
                        liability['expense']
                    )
                    self.financial_statement['expenses'] += liability['expense']
                    self.next_liability_id += 1
                elif liability['operation'] == 'update':
                    liability_id = liability['id'] # always be 0 for bank loans
                    if liability_id in self.financial_statement['liabilities']:
                        self.financial_statement['liabilities'][liability_id].cost += liability['cost']
                        self.financial_statement['liabilities'][liability_id].expense += liability['expense']
                        self.financial_statement['expenses'] += liability['expense']    
                else:
                    liability_id = liability['id']
                    if liability_id in self.financial_statement['liabilities']:
                        removed_liability = self.financial_statement['liabilities'][liability_id]
                        self.financial_statement['expenses'] -= removed_liability.expense
                        del self.financial_statement['liabilities'][liability_id]

    def take_turn(self):
        while(self.inp.get_shared_opp().get("shared_opp") == 'y'):
            self.opportunity()
        self.repay_borrow()
        card = self.inp.get_card_type().get("card")
        if card == 'shared opportunity':
            while(self.inp.get_has_asset().get("has_asset") == 'y'):
                self.opportunity()
        elif card == 'deal':
            self.deal()
        elif card == 'charity':
            self.charity()
        elif card == 'no deal':
            self.no_deal()
        else:
            print("Invalid card")
        self.repay_borrow()

    def run_game(self):
        starting_state = self.inp.get_starting_state()
        self.financial_statement['cash'] = starting_state.get('cash', 0)
        self.financial_statement['income'] = starting_state.get('income', 0)
        self.financial_statement['expenses'] = starting_state.get('expenses', 0)
        self.financial_statement['liabilities'][0] = Liability(0, 0)
        liabilities = starting_state.get('liabilities', [])
        for liability in liabilities:
            cost = liability.get('cost', 0)
            expense = liability.get('expense', 0)
            self.financial_statement['liabilities'][self.next_liability_id] = Liability(cost, expense)
            self.financial_statement['expenses'] += expense
            self.next_liability_id += 1
        while True:
            self.take_turn()
            self.inp.output_financials(self.financial_statement)
            if self.inp.get_continue().get("cont") == 'n':
                break
        return

if __name__ == "__main__":
    llm = ChatOllama(
        model="llama3.2",
        temperature=0,
    )
    inp = ConsoleInput()
    game = CashflowGame(llm, inp)
    game.run_game()

