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

    write_df(df, "gl_postings_fact")
    print("✅ Finance data loaded")


if __name__ == "__main__":
    main()
