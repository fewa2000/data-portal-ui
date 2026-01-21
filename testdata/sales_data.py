from faker import Faker
import pandas as pd
import random
from datetime import timedelta
from db import write_df

REGIONS = ["DACH", "Nordics", "UK", "France"]
CATEGORIES = ["Electronics", "Clothing", "Home", "Sports"]
CHANNELS = ["Online", "Retail", "Wholesale"]

ROWS = 50_000

# FIXED: Create visitor pool for realistic conversion rate
# Target conversion rate: ~3.5%
# If we have 50,000 orders and want 3.5% conversion, we need ~1,428,571 visitors
CONVERSION_RATE = 0.035
VISITOR_POOL_SIZE = int(ROWS / CONVERSION_RATE)


def main():
    fake = Faker()
    
    # Generate pool of visitor IDs (representing all website visitors)
    print(f"Generating {VISITOR_POOL_SIZE:,} unique visitors for {ROWS:,} orders...")
    print(f"Expected conversion rate: {CONVERSION_RATE * 100:.1f}%")
    VISITOR_POOL = [fake.uuid4() for _ in range(VISITOR_POOL_SIZE)]
    
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
            # FIXED: Select from visitor pool instead of generating new UUID every time
            "visitor_id": random.choice(VISITOR_POOL)
        })

    df = pd.DataFrame(data)
    
    # Verify conversion rate
    actual_conversion = (df['order_id'].nunique() / df['visitor_id'].nunique()) * 100
    print(f"Actual conversion rate: {actual_conversion:.2f}%")
    print(f"Unique visitors: {df['visitor_id'].nunique():,}")
    print(f"Total orders: {df['order_id'].nunique():,}")

    write_df(df, "sales_orders_fact")
    print("✅ Sales data loaded")


if __name__ == "__main__":
    main()