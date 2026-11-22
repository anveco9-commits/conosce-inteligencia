import os
from sqlalchemy import create_engine

host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")

connection_string = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)

engine = create_engine(connection_string)

with engine.connect() as conn:
    print("Conexion exitosa con Neon")
