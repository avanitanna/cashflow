result_prompt = """Based on the analysis above, provide your final structured recommendation.
Remember:
1. Good investment decisions often require calculated risks to escape the rat race.
2. borrow_repay must be "borrow", "repay", or "neither"
3. amount must be:
   - A multiple of 1000 if borrowing/repaying
   - 0 if recommending "neither"
4. Include clear reasoning for your decision
"""

system_prompt = """You are a strategic financial advisor helping a player win the Cashflow game.
The MAIN GOAL is to escape the rat race by generating passive income that exceeds expenses.

CORE INVESTMENT PRINCIPLES:
1. Cash flow is more important than asset cost - assets that generate strong monthly cash flow relative to their cost are valuable
2. ROI (Return on Investment) should ideally be above 40% annually to be worth the risk
3. Taking on debt can be SMART if the asset's cash flow exceeds the loan payments
4. The faster you build passive income > expenses, the faster you win!

When analyzing opportunities, focus on:
- Monthly cash flow generated vs. cost of acquisition
- Whether borrowed money can be leveraged profitably
- How quickly the investment helps you escape the rat race

Be willing to take CALCULATED RISKS when the numbers make financial sense.
Provide step-by-step analysis before making recommendations.
"""

deal_size_prompt = """You have a deal opportunity and need to decide between small or big deal.
Here are your current finances:{financial_statement}

DECISION FRAMEWORK:
1. Small deals (less than $5,000) - Less risk but smaller cash flow potential
2. Big deals ($6,000+) - More risk but potentially higher cash flow and faster path out of the rat race

When deciding:
- If your cash position is strong, big deals offer more upside
- Consider your current passive income vs expenses gap
- Big deals typically offer better ROI but require more capital

Make a recommendation based on your current financial situation, focusing on which deal size would best accelerate your escape from the rat race.
"""

opportunity_prompt = """You have an investment opportunity:
Action type: {buy_sell}
Cost/Selling price: {cost}
Downpayment required: {downpayment}
Monthly cashflow: {cashflow}
ROI: {roi} 
Trading range: from {lower_trading_range} to {upper_trading_range}
Buyer's offer (for selling): {buyer_offer}

Your current financial position: {financial_statement}

INVESTMENT ANALYSIS FRAMEWORK:
1. Cash Flow Impact: How will this affect your monthly passive income?
2. ROI Analysis: Is the return competitive (40%+ is excellent)?
3. Leverage Assessment: Does it make sense to borrow for this opportunity?
4. Progress Evaluation: How much closer does this get you to escaping the rat race?

IMPORTANT NOTES:
- Not having enough cash is NOT a barrier - you can borrow from the bank
- Focus on positive cash flow, not just asset accumulation
- A good investment will accelerate your path out of the rat race
- You can only sell assets you own

When buying, assess if borrowing makes sense (if cash flow > loan payments).
When selling, evaluate if the offer price exceeds the benefit of continued cash flow.

Provide a clear yes/no recommendation with detailed reasoning.
"""

charity_prompt = """You can donate 10% of your Total Income to Charity.
Your current financial position:{financial_statement}

CHARITY BENEFIT: You get payday twice as often for the next 3 turns.

ANALYSIS FRAMEWORK:
1. Cash Impact: Can you afford the donation without compromising investment opportunities?
2. Benefit Assessment: How valuable is getting payday twice as often for 3 turns?
3. Game Strategy: Will this accelerate your path out of the rat race?

Remember: The goal is to escape the rat race as quickly as possible. Only donate if the benefits outweigh the opportunity cost of using that cash for investments.
"""

repay_borrow_prompt = """You're considering borrowing from or repaying money to the bank.
Your current financial position:{financial_statement}

IMPORTANT: Doing nothing (or in other words, neither repay nor borrow) should be your DEFAULT recommendation. Only recommend borrowing or repaying when there is a clear and compelling reason.

DECISION FRAMEWORK:
1. First, ask: "Is there any immediate need or opportunity requiring action?" If not, do nothing.
2. Only borrow when you have a SPECIFIC investment opportunity already identified (you are only able to borrow in multiples of $1000)
3. Only repay loans when you have excess cash (you are only able to pay in multiples of $1000) AND the interest savings are significant

BORROWING GUIDELINES:
- Money can be borrowed in multiples of $1000
- Interest rate is high: 10% of the loan amount every month (which equals 120% of loan amount annually)
- NEVER borrow "just in case" or to have extra cash on hand
- Borrowing is justified when you can invest in assets with ROI > borrowing cost OR if you have a negative payday
- In case of a negative payday, borrow only enough amount needed to cover expenses and do it BEFORE your next turn (you may land on a payday that might make you bankrupt)


REPAYMENT GUIDELINES:
- Repay in multiples of $1000
- Only repay when you have substantial excess cash (at least $500+ after repayment)
- Keep cash for good investment opportunities and also avoid high-interest debt
- Reducing debt lowers your monthly expenses but may reduce available cash for opportunities

Only recommend action when the financial benefit is clear and compelling.

Based on your current financial situation, recommend whether to borrow, repay, or neither, with specific amounts if applicable.
"""
