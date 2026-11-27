import pandas as pd
from sqlalchemy import create_engine

# Conexión Neon
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_KUCFxuvDW46f@ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech:5432/neondb?sslmode=require"
)

# Archivo proveedores
url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/proveedores/2026/PROVEEDORES2026_0.xlsx"

df = pd.read_excel(url, engine="openpyxl")

print(df.columns.tolist())

# Renombrado mínimo
if "RUC_PROVEEDOR" in df.columns:
    df = df.rename(columns={"RUC_PROVEEDOR": "ruc_proveedor"})

if "PROVEEDOR" in df.columns:
    df = df.rename(columns={"PROVEEDOR": "proveedor"})

# Campos por defecto
if "ruc_proveedor" not in df.columns:
    df["ruc_proveedor"] = None

if "proveedor" not in df.columns:
    df["proveedor"] = None

if "estado_proveedor" not in df.columns:
    df["estado_proveedor"] = None

# Estructura final
df = df[
    [
        "ruc_proveedor",
        "proveedor",
        "estado_proveedor"
    ]
]

# Eliminar duplicados
df = df.drop_duplicates()

# Limpiar tabla
with engine.begin() as conn:
    conn.exec_driver_sql(
        "TRUNCATE TABLE fact_proveedor_individual RESTART IDENTITY"
    )

# Cargar
df.to_sql(
    "fact_proveedor_individual",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print("PROVEEDORES CARGADOS:", len(df))
