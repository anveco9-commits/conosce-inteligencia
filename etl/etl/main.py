from sqlalchemy import create_engine

host = "ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech"
database = "neondb"
user = "neondb_owner"
password = "npg_KUCFxuvDW46f"
port = "5432"

cadena = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)

engine = create_engine(cadena)

with engine.connect() as conexion:
    print("CONEXION EXITOSA A NEON")
