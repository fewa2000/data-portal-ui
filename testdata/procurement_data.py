from faker import Faker
import pandas as pd
import random
from datetime import timedelta
from db import write_df

SUPPLIERS = ["Supplier A", "Supplier B", "Supplier C", "Supplier D"]
MATERIAL_GROUPS = ["Raw Materials", "Components", "Services", "Equipment"]
PLANTS = ["Plant 100", "Plant 200", "Plant 300"]

ROWS = 25_000


def main():
    fake = Faker()
    data = []

    start_date = fake.date_between(start_date="-18M", end_date="-12M")

    for i in range(ROWS):
        purchase_date = start_date + timedelta(days=random.randint(0, 365))
        requested_delivery = purchase_date + timedelta(days=random.randint(5, 20))

        # 92% on-time delivery
        on_time = random.random() < 0.92
        actual_delivery = requested_delivery if on_time else requested_delivery + timedelta(days=random.randint(1, 10))

        spend = round(random.uniform(200, 25_000), 2)

        data.append({
            "purchase_order_id": i + 1,
            "purchase_date": purchase_date,
            "supplier": random.choice(SUPPLIERS),
            "material_group": random.choice(MATERIAL_GROUPS),
            "plant": random.choice(PLANTS),
            "spend": spend,
            "requested_delivery_date": requested_delivery,
            "actual_delivery_date": actual_delivery
        })

    df = pd.DataFrame(data)

    write_df(df, "procurement_orders_fact")
    print("✅ Procurement data loaded")


if __name__ == "__main__":
    main()
