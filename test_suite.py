# create data aka turns
# run game
# figure out how to test for the decisions (workflow just prints stuff out
# add additional optional parameter to cashflowgame which is the out parameter for all print statements -> can make it write to some "file" i control

import input_wrappers
import ratrace_workflow
from langchain_ollama import ChatOllama
from multiprocessing import Pool, Manager
from typing import Dict, Any, List
import queue

def tests():
    all_tests = []
    # simple test
    simple_test = [
        input_wrappers.Turn(card="deal", choice=1, buy_sell="buy", cost=50000,
                            downpayment=1000, cashflow=500, lower_trading_range=65000,
                            upper_trading_range=135000, cash=500, income=3750,
                            expenses=950, liabilities=[{"cost":50000, "expense":1000},
                                                       {"cost":1500, "expense":20}],
                            opp_decision=True, go_big=True)
    ]

    inp = input_wrappers.TestInput(simple_test)
    all_tests.append(inp)

    # simple test
    simple_test_2 = [
        input_wrappers.Turn(card="deal", choice=1, buy_sell="buy", cost=135000,
                            downpayment=20000, cashflow=100, lower_trading_range=65000,
                            upper_trading_range=135000, cash=500, income=3750,
                            expenses=950, liabilities=[{"cost":50000, "expense":1000},
                                                       {"cost":1500, "expense":20}],
                            opp_decision=False, go_big=True),
        input_wrappers.Turn(card="deal", choice=1, buy_sell="buy", cost=85000,
                            downpayment=7000, cashflow=400, lower_trading_range=65000,
                            upper_trading_range=135000, cash=500, income=3750,
                            expenses=950, liabilities=[{"cost":50000, "expense":1000},
                                                       {"cost":1500, "expense":20}],
                            opp_decision=True, go_big=True),
        input_wrappers.Turn(card="no deal", cost=-1480, baby="no", borrow_repay="repay",
                            amount=1000),
        input_wrappers.Turn(card="no deal", cost=-1480, baby="no", borrow_repay="repay",
                            amount=2000),
        input_wrappers.Turn(card="shared opportunity",  choice=1, buy_sell="sell",
                            asset_id=0, cost=135000, lower_trading_range=65000,
                            upper_trading_range=135000, opp_decision=True)
    ]

    inp = input_wrappers.TestInput(simple_test_2)
    all_tests.append(inp)

    # test 3
    test_3 = [
        input_wrappers.Turn(card="no deal", cash=400, income=13200, expenses=3420+2880,
                            liabilities=[{"cost":202000, "expense":1900},
                                         {"cost":19000, "expense":380},
                                         {"cost":9000, "expense":270},
                                         {"cost":1000, "expense": 50}],
                            cost=200, baby="no"),
        input_wrappers.Turn(card="no deal", cost=-4300, baby="no"),
        input_wrappers.Turn(card="no deal", cost=640, baby="yes"),
        input_wrappers.Turn(card="no deal", cost=-3660, baby="no"),
        input_wrappers.Turn(card="deal", go_big=True, choice=1, buy_sell="buy",
                            cost=70000, downpayment=20000, cashflow=500,
                            lower_trading_range=65000, upper_trading_range=135000,
                            opp_decision=False),
        input_wrappers.Turn(card="no deal", cost=-3660, baby="no"),
        input_wrappers.Turn(card="no deal", cost=100, baby="no"),
        input_wrappers.Turn(card="deal", go_big=True, choice=1, buy_sell="buy",
                            cost=60000, downpayment=12000, cashflow=400,
                            lower_trading_range=50000, upper_trading_range=90000,
                            opp_decision=True),
        input_wrappers.Turn(card="no deal", cost=-3860, baby="no"),
        input_wrappers.Turn(card="deal", go_big=True, choice=1, buy_sell="buy",
                            cost=65000, downpayment=7000, cashflow=150,
                            lower_trading_range=65000, upper_trading_range=135000,
                            opp_decision=True),
        input_wrappers.Turn(card="no deal", cost=-3810, baby="no", borrow_repay="repay",
                            amount=4000)
    ]

    inp = input_wrappers.TestInput(test_3)
    all_tests.append(inp)

    # test 4
    test_4 = [
        input_wrappers.Turn(card="no deal", cash=400, income=4900, expenses=1050+1090,
                            liabilities=[{"cost":75000, "expense":7000},
                                         {"cost":7000, "expense":140},
                                         {"cost":4000, "expense":120},
                                         {"cost":1000, "expense": 50}],
                            cost=-1750, baby="no"),
        input_wrappers.Turn(card="no deal", cost=-1750, baby="no"),
        input_wrappers.Turn(card="deal", go_big=True, choice=1, buy_sell="buy",
                            cost=70000, downpayment=9000, cashflow=300,
                            lower_trading_range=65000, upper_trading_range=135000,
                            opp_decision=True),
        input_wrappers.Turn(card="no deal", cost=3750, baby="no"),
        input_wrappers.Turn(card="no deal", cost=-1150, baby="no"),
        input_wrappers.Turn(card="shared opportunity", go_big=True, choice=1, buy_sell="sell",
                            cost=100000, asset_id=0, borrow_repay="repay", amount=9000,
                            lower_trading_range=65000, upper_trading_range=135000,
                            opp_decision=True),
        input_wrappers.Turn(card="charity", charity_decision=True),
        input_wrappers.Turn(card="no deal", cost=-1750, baby="no"),
        input_wrappers.Turn(card="no deal", cost=-1750, baby="no"),
        input_wrappers.Turn(card="no deal", cost=-1750, baby="no"),
        input_wrappers.Turn(card="no deal", cost=300, baby="no"),
        input_wrappers.Turn(card="no deal", cost=-1750, baby="no"),
        input_wrappers.Turn(card="deal", go_big=True, choice=1, buy_sell="buy",
                            cost=65000, downpayment=8000, cashflow=300,
                            lower_trading_range=65000, upper_trading_range=135000,
                            opp_decision=True),
        input_wrappers.Turn(card="deal", go_big=True, choice=1, buy_sell="buy",
                            cost=25000, downpayment=25000, cashflow=1000,
                            opp_decision=True),
        input_wrappers.Turn(card="no deal", cost=-3050, baby="no"),
    ]

    inp = input_wrappers.TestInput(test_4)
    all_tests.append(inp)

    # test 5
    test_5 = [
        input_wrappers.Turn(card="deal", cash=710, income=2500, expenses=460+570,
                            liabilities=[{"cost":38000, "expense":400},
                                         {"cost":4000, "expense":80},
                                         {"cost":2000, "expense":60},
                                         {"cost":1000, "expense":50}],
                            choice=1, go_big=False, cost=5000, cashflow=0, buy_sell="buy",
                            downpayment=5000, lower_trading_range=0, upper_trading_range=0,
                            opp_decision=False),
        input_wrappers.Turn(card="no deal", cost=-880, baby="no"),
        input_wrappers.Turn(card="deal", go_big=False, choice=1, buy_sell="buy",
                            cost=3000, downpayment=3000, cashflow=0,
                            opp_decision=False),
        input_wrappers.Turn(card="no deal", cost=140, baby="yes"),
        input_wrappers.Turn(card="no deal", cost=-740, baby="no"),
        input_wrappers.Turn(card="deal", go_big=False, choice=2, buy_sell="buy",
                            cost=40, cashflow=0, lower_trading_range=5,
                            upper_trading_range=40, opp_decision=False),
        input_wrappers.Turn(card="deal", go_big=False, choice=4, buy_sell="buy",
                            cost=4000, cashflow=20, lower_trading_range=4000,
                            upper_trading_range=4000, opp_decision=False),
        input_wrappers.Turn(card="no deal", cost=-740, baby="no"),
        input_wrappers.Turn(card="deal", go_big=False, choice=2, buy_sell="buy",
                            cost=20, cashflow=0, lower_trading_range=10,
                            upper_trading_range=40, opp_decision=False),
        input_wrappers.Turn(card="deal", go_big=False, choice=2, buy_sell="buy",
                            cost=30, cashflow=0, lower_trading_range=5,
                            upper_trading_range=30, opp_decision=False),
    ]

    inp = input_wrappers.TestInput(test_5)
    all_tests.append(inp)

    return all_tests

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

def process_test_case(args):
    test_idx, inp = args
    print(f"Starting test {test_idx}")
    game = ratrace_workflow.CashflowGame(llm, inp)
    game.run_game()

    turn_stats = []
    for i, turn in enumerate(inp.stats):
        s = 0
        t = 0
        for _, value in turn.items():
            if value:
                s += 1
            t += 1
        turn_stats.append({
            'turn_idx': i,
            'stats': turn,
            'success_rate': s/t if t > 0 else 0
        })

    return {
        'test_idx': test_idx,
        'turn_stats': turn_stats
    }

def main():
    inps = tests()
    stats = {}

    # Create a process pool
    with Pool() as pool:
        # Map test cases to processes
        results = pool.map(process_test_case, enumerate(inps))

        # Process results as they come in
        for result in results:
            test_idx = result['test_idx']
            print("-" * 100)
            print(f"Results for test {test_idx}")

            for turn_data in result['turn_stats']:
                turn_idx = turn_data['turn_idx']
                turn_stats = turn_data['stats']
                success_rate = turn_data['success_rate']

                print(f"Turn {turn_idx}:")
                print(f"Stats: {turn_stats}")
                print(f"Success rate for turn {turn_idx}: {success_rate}")

                # Aggregate stats
                for key, value in turn_stats.items():
                    if key not in stats:
                        stats[key] = {"success": 0, "total": 0}
                    if value:
                        stats[key]["success"] += 1
                    stats[key]["total"] += 1

            print("-" * 100)

    # Print final statistics
    success = 0
    total = 0
    for key, value in stats.items():
        success += value['success']
        total += value['total']
        print(f"{key}: {value['success']}/{value['total']} ({value['success']/value['total']})")
    print(f"Total success rate: {success/total}")


if __name__ == "__main__":
    main()

