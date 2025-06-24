from typing import Dict, Any, List

from langchain_core.messages import BaseMessage

class InputOutput:
    def get_opportunity(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")

    def get_no_deal(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")

    def get_card_type(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")

    def get_shared_opp(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")

    def get_starting_state(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")

    def get_has_asset(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")

    def get_continue(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")

    def output_financials(self, financials: dict):
        raise NotImplementedError("Subclasses must implement this method")

    def print_deal_rec(self, rec: Any):
        raise NotImplementedError("Subclasses must implement this method")

    def note_loan(self):
        raise NotImplementedError("Subclasses must implement this method")

    def print_deal_size_rec(self, rec: Any):
        raise NotImplementedError("Subclasses must implement this method")

    def print_charity_rec(self, rec: Any):
        raise NotImplementedError("Subclasses must implement this method")

    def print_borrow_repay_rec(self, rec: Any):
        raise NotImplementedError("Subclasses must implement this method")

    def print_message(self, message: BaseMessage):
        raise NotImplementedError("Subclasses must implement this method")

class ConsoleInput(InputOutput):
    def get_opportunity(self) -> Dict[str, Any]:
        print("\nOpportunity Options:")
        print("1. real estate")
        print("2. stock")
        print("3. land")
        print("4. CD")
        print("5. business")
        choice = input("Enter your choice (1-5): ")
        buy_sell = input("Buy or sell? (buy/sell): ")
        asset_id = input("Enter asset ID: ")
        cost = input("Enter cost of opportunity: ")
        downpayment = input("Enter downpayment of opportunity: ")
        cashflow = input("Enter cashflow of opportunity: ")
        lower_trading_range = input("Enter lower trading range of opportunity: ")
        upper_trading_range = input("Enter upper trading range of opportunity: ")
        buyer_offer = input("Enter buyer offer: ")
        # Convert to int where appropriate
        def to_int(val):
            try:
                return int(val)
            except ValueError:
                return val
        return {
            "choice": to_int(choice),
            "buy_sell": buy_sell,
            "asset_id": to_int(asset_id),
            "cost": to_int(cost),
            "downpayment": to_int(downpayment),
            "cashflow": to_int(cashflow),
            "lower_trading_range": lower_trading_range,
            "upper_trading_range": upper_trading_range,
            "buyer_offer": buyer_offer
        }

    def get_no_deal(self) -> Dict[str, Any]:
        cost = int(input("Enter cost incurred or payday amount."
                         " If you are paying money, enter positive value. If you are gaining, enter negative value: "))
        baby = input("Is this a new baby? (yes/no)")
        return {
            "cost": cost,
            "baby": baby
        }

    def get_card_type(self) -> Dict[str, Any]:
        card = input("Which card did you draw? (shared opportunity/deal/charity/no deal)").lower()
        if card not in ["shared opportunity", "deal", "charity", "no deal"]:
            print("Invalid card")
            return self.get_card_type()
        return {"card": card}

    def get_shared_opp(self) -> Dict[str, Any]:
        shared_opp = input("Is it a shared opportunity? (y/n)")
        return {"shared_opp": shared_opp}

    def get_starting_state(self) -> Dict[str, Any]:
        cash = int(input("Enter your starting cash: "))
        income = int(input("Enter your starting income: "))
        expenses = int(input("Enter your starting expenses (this will likely be taxes + other expenses): "))
        liabilities = []
        while(input("Do you have any liabilities? (y/n)") == 'y'):
            cost = int(input("Enter cost of liability: "))
            expense = int(input("Enter expense of liability: "))
            liabilities.append({"cost": cost, "expense": expense})
        return {"cash": cash, "income": income, "expenses": expenses, "liabilities": liabilities}

    def get_has_asset(self) -> Dict[str, Any]:
        has_asset = input("Do you have the applicable asset? (y/n)")
        return {"has_asset": has_asset}

    def get_continue(self) -> Dict[str, Any]:
        cont = input("Do you want to continue? (y/n)")
        return {"cont": cont}

    def financials_to_string(self, financial_statement):
        output = []

        # Basic financial info
        output.append(f"Cash: ${financial_statement['cash']}")
        output.append(f"Income: ${financial_statement['income']}")
        output.append(f"Expenses: ${financial_statement['expenses']}")

        # Assets section
        output.append("\nAssets:")
        for asset_id, asset in financial_statement['assets'].items():
            output.append(f"  ID {asset_id}:")
            output.append(f"    Cost: ${asset.cost}")

            output.append(f"    Cashflow: ${asset.cashflow}")

        # Liabilities section
        output.append("\nLiabilities:")
        for liability_id, liability in financial_statement['liabilities'].items():
            output.append(f"  ID {liability_id}:")
            output.append(f"    Cost: ${liability.cost}")
            output.append(f"    Expense: ${liability.expense}")

        return "\n".join(output)

    def output_financials(self, financials: dict):
        print(self.financials_to_string(financials))

    def print_deal_rec(self, rec):
        print(f"\nBased on your financial position, LLM recommends: {rec.yes_or_no}\nReasoning: {rec.reasoning}")

    def note_loan(self):
        print("Not enough cash, taking a loan")

    def print_deal_size_rec(self, rec: Any):
        print(f"\nBased on your financial position, LLM recommends: big deal: {rec.big}\nReasoning: {rec.reasoning}")

    def print_charity_rec(self, rec: Any):
        print(f"\nBased on your financial position, LLM recommends: {rec.yes_or_no}\nReasoning: {rec.reasoning}")

    def print_borrow_repay_rec(self, rec: Any):
        print(f"\nBased on your financial position, LLM recommends: {rec.borrow_repay} ${rec.amount}\nReasoning: {rec.reasoning}")

    def print_message(self, message: BaseMessage):
        message.pretty_print()

class Turn:
    def __init__(self, choice: int = 0, buy_sell: str = "", asset_id: int = -1,
                 cost: int = 0, downpayment: int = 0, cashflow: int = 0,
                 lower_trading_range: int = 0, upper_trading_range: int = 0,
                 buyer_offer: int = 0, baby: str = "", card: str = "",
                 shared_opp: str = "", cash: int = 0, income: int = 0,
                 expenses: int = 0, liabilities: List[Dict[str, int]] = {},
                 has_asset: str = "", cont: str = "", go_big: bool = False,
                 opp_decision: bool = False, charity_decision: bool = False,
                 borrow_repay: str = "neither", amount: int = 0):
        self.choice = choice
        self.buy_sell = buy_sell
        self.asset_id = asset_id
        self.cost = cost
        self.downpayment = downpayment
        self.cashflow = cashflow
        self.lower_trading_range = lower_trading_range
        self.upper_trading_range = upper_trading_range
        self.buyer_offer = buyer_offer
        self.baby = baby
        self.card = card
        self.shared_opp = shared_opp
        self.cash = cash
        self.income = income
        self.expenses = expenses
        self.liabilities = liabilities
        self.has_asset = has_asset
        self.cont = cont
        self.go_big = go_big
        self.opp_decision = opp_decision
        self.charity_decision = charity_decision
        self.borrow_repay = borrow_repay
        self.amount = amount

class TestInput(InputOutput):
    def __init__(self, turns: List[Turn]):
        self.turns: List[Turn] = turns
        self.current_turn = 0
        self.stats = []

    def get_opportunity(self) -> Dict[str, Any]:
        t = self.turns[self.current_turn]
        return {
            "choice": t.choice,
            "buy_sell": t.buy_sell,
            "asset_id": t.asset_id,
            "cost": t.cost,
            "downpayment": t.downpayment,
            "cashflow": t.cashflow,
            "lower_trading_range": t.lower_trading_range,
            "upper_trading_range": t.upper_trading_range,
            "buyer_offer": t.buyer_offer
        }


    def get_no_deal(self) -> Dict[str, Any]:
        t = self.turns[self.current_turn]
        return {
            "cost": t.cost,
            "baby": t.baby
        }

    def get_card_type(self) -> Dict[str, Any]:
        t = self.turns[self.current_turn]
        return {"card": t.card}

    def get_shared_opp(self) -> Dict[str, Any]:
        t = self.turns[self.current_turn]
        return {"shared_opp": t.shared_opp}

    def get_starting_state(self) -> Dict[str, Any]:
        t = self.turns[self.current_turn]
        return {
            "cash": t.cash,
            "income": t.income,
            "expenses": t.expenses,
            "liabilities": t.liabilities
        }

    def get_has_asset(self) -> Dict[str, Any]:
        t = self.turns[self.current_turn]
        return {"has_asset": t.has_asset}

    def get_continue(self) -> Dict[str, Any]:
        print(f"current turn: {self.current_turn}, starting new turn")
        self.current_turn += 1
        if self.current_turn < len(self.turns):
            return {"cont": "y"}
        else:
            return {"cont": "n"}

    def output_financials(self, financials: dict):
        # nothing to do here
        pass

    def print_deal_rec(self, rec: Any):
        if rec is None:
            if len(self.stats) == self.current_turn:
                self.stats.append({})
            self.stats[self.current_turn]['opp_decision'] = False
            return
        t = self.turns[self.current_turn]
        if len(self.stats) == self.current_turn:
            self.stats.append({})
        self.stats[self.current_turn]['opp_decision'] = True if t.opp_decision == rec.yes_or_no else False

    def note_loan(self):
        # could check for this, but not for now
        pass

    def print_deal_size_rec(self, rec: Any):
        if rec is None:
            if len(self.stats) == self.current_turn:
                self.stats.append({})
            self.stats[self.current_turn]['big_small'] = False
            return
        t = self.turns[self.current_turn]
        if len(self.stats) == self.current_turn:
            self.stats.append({})
        self.stats[self.current_turn]['big_small'] = True if t.go_big == rec.big else False

    def print_charity_rec(self, rec: Any):
        if rec is None:
            if len(self.stats) == self.current_turn:
                self.stats.append({})
            self.stats[self.current_turn]['charity_decision'] = False
            return
        t = self.turns[self.current_turn]
        if len(self.stats) == self.current_turn:
            self.stats.append({})
        self.stats[self.current_turn]['charity_decision'] = True if t.charity_decision == rec.yes_or_no else False

    def print_borrow_repay_rec(self, rec: Any):
        if rec is None:
            if len(self.stats) == self.current_turn:
                self.stats.append({})
            self.stats[self.current_turn]['borrow_repay'] = False
            self.stats[self.current_turn]['amount'] = False
            return
        t = self.turns[self.current_turn]
        if len(self.stats) == self.current_turn:
            self.stats.append({})
        self.stats[self.current_turn]['borrow_repay'] = True if t.borrow_repay == rec.borrow_repay else False
        if t.borrow_repay in ['borrow', 'repay']:
            self.stats[self.current_turn]['amount'] = True if t.amount == rec.amount else False

    def print_message(self, message: BaseMessage):
        # nothing to do here
        pass
    
    