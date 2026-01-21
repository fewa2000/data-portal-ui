from faker import Faker
import pandas as pd
import random
from datetime import timedelta
from db import write_df

REGIONS = ["DACH", "Nordics", "UK", "France"]
CATEGORIES = ["Electronics", "Clothing", "Home", "Sports"]
CHANNELS = ["Online", "Retail", "Wholesale"]

ROWS = 50_000


def main():
    fake = Faker()
    data = []

    start_date = fake.date_between(start_date="-18M", end_date="-12M")

    for i in range(ROWS):
        order_date = start_date + timedelta(days=random.randint(0, 365))

        revenue = round(random.uniform(20, 600), 2)

        data.append({
            "order_id": i + 1,
            "order_date": order_date,
            "region": random.choices(REGIONS, weights=[0.4, 0.2, 0.25, 0.15])[0],
            "product_category": random.choice(CATEGORIES),
            "channel": random.choices(CHANNELS, weights=[0.65, 0.25, 0.1])[0],
            "revenue": revenue,
            "visitor_id": fake.uuid4() if random.random() < 0.35 else fake.uuid4()
        })

    df = pd.DataFrame(data)

    write_df(df, "sales_orders_fact")
    print("✅ Sales data loaded")


if __name__ == "__main__":
    main()
