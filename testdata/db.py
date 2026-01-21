from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://user:password@localhost:5432/dataportal"

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
