from sqlalchemy import create_engine, text

DB_URL = "postgresql+psycopg2://postgres:password@localhost:5432/data_portal"

engine = create_engine(DB_URL)

def write_df(df, table):
    df.to_sql(
        table,
        engine,
        schema="mart",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000
    )


with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database();"))
    print(result.fetchone())
