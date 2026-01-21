import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load .env file from project root
_project_root = Path(__file__).parent.parent
_env_file = _project_root / ".env"
if _env_file.exists():
    load_dotenv(_env_file)

DB_URL = os.environ["DATABASE_URL"]

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
