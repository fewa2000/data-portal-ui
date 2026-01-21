from faker import Faker
import pandas as pd
import random
from datetime import date
from db import write_df

COMPANY_CODES = ["1000", "2000"]
COST_CENTERS = ["CC100", "CC200", "CC300", "CC400"]
ACCOUNTS = {
    "REVENUE": ["4000", "4010"],
    "OPERATING_INCOME": ["4100"],
    "EXPENSE": ["5000", "5100", "5200"]
}

ROWS = 40_000


def main():
    fake = Faker()
    data = []

    print(f"Generating {ROWS:,} GL postings...")
    print(f"Expected distribution: Revenue (45%), Operating Income (15%), Expense (40%)")

    for i in range(ROWS):
        posting_period = date(
            year=random.choice([2024, 2025]),
            month=random.randint(1, 12),
            day=1
        )

        account_type = random.choices(
            ["REVENUE", "OPERATING_INCOME", "EXPENSE"],
            weights=[0.45, 0.15, 0.4]
        )[0]

        amount = random.uniform(500, 20_000)

        if account_type == "EXPENSE":
            amount *= -1

        data.append({
            "posting_id": i + 1,
            "posting_period": posting_period,
            "company_code": random.choice(COMPANY_CODES),
            "cost_center": random.choice(COST_CENTERS),
            "account": random.choice(ACCOUNTS[account_type]),
            "account_type": account_type,
            "amount": round(amount, 2)
        })

    df = pd.DataFrame(data)

    # Calculate statistics
    revenue_count = len(df[df['account_type'] == 'REVENUE'])
    operating_income_count = len(df[df['account_type'] == 'OPERATING_INCOME'])
    expense_count = len(df[df['account_type'] == 'EXPENSE'])
    
    total_revenue = df[df['account_type'] == 'REVENUE']['amount'].sum()
    total_operating_income = df[df['account_type'] == 'OPERATING_INCOME']['amount'].sum()
    total_expenses = df[df['account_type'] == 'EXPENSE']['amount'].sum()
    net_income = df['amount'].sum()
    
    operating_margin = (total_operating_income / total_revenue * 100) if total_revenue > 0 else 0

    print(f"\nActual distribution:")
    print(f"  Revenue: {revenue_count:,} postings ({revenue_count/ROWS*100:.1f}%)")
    print(f"  Operating Income: {operating_income_count:,} postings ({operating_income_count/ROWS*100:.1f}%)")
    print(f"  Expense: {expense_count:,} postings ({expense_count/ROWS*100:.1f}%)")
    
    print(f"\nFinancial Summary:")
    print(f"  Total Revenue: ${total_revenue:,.2f}")
    print(f"  Operating Income: ${total_operating_income:,.2f}")
    print(f"  Total Expenses: ${abs(total_expenses):,.2f}")
    print(f"  Net Income: ${net_income:,.2f}")
    print(f"  Operating Margin: {operating_margin:.1f}%")

    write_df(df, "gl_postings_fact")
    print("\n✅ Finance data loaded")


if __name__ == "__main__":
    main()