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

    print(f"Generating {ROWS:,} purchase orders...")
    print(f"Expected on-time delivery rate: 92%")

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

    # Calculate statistics
    on_time_count = len(df[df['actual_delivery_date'] <= df['requested_delivery_date']])
    actual_on_time_rate = (on_time_count / len(df) * 100)
    total_spend = df['spend'].sum()
    avg_po_value = df['spend'].mean()
    
    # Supplier distribution
    supplier_counts = df['supplier'].value_counts()
    
    print(f"\nActual on-time delivery rate: {actual_on_time_rate:.2f}%")
    print(f"On-time orders: {on_time_count:,} / {len(df):,}")
    
    print(f"\nProcurement Summary:")
    print(f"  Total Spend: ${total_spend:,.2f}")
    print(f"  Average PO Value: ${avg_po_value:,.2f}")
    print(f"  Total Purchase Orders: {len(df):,}")
    
    print(f"\nSupplier Distribution:")
    for supplier in SUPPLIERS:
        count = supplier_counts.get(supplier, 0)
        supplier_spend = df[df['supplier'] == supplier]['spend'].sum()
        print(f"  {supplier}: {count:,} POs (${supplier_spend:,.2f})")

    write_df(df, "procurement_orders_fact")
    print("\n✅ Procurement data loaded")


if __name__ == "__main__":
    main()