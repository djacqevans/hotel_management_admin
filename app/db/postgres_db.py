import os
from typing import Optional

def get_database_uri() -> str:
    host = os.environ.get("PG_HOST", "localhost")
    port = os.environ.get("PG_PORT", "5432")
    username = os.environ.get("PG_USERNAME", "postgres")
    password = os.environ.get("PG_PASSWORD", "postgres")
    database_name = os.environ.get("PG_DB", "hotel_management")
    database_schema = os.environ.get("PG_SCHEMA", "public")
    
    return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}?options=-csearch_path%3D{database_schema}"

