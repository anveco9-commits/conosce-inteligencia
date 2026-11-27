import pandas as pd
from sqlalchemy import create_engine

# Conexión Neon
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_KUCFxuvDW46f@ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech:5432/neondb?sslmode=require"
)

# Archivo consorcios
url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/consorcios/2026/CONSORCIO2026_0.xlsx"

df = pd.read_excel(url, engine="openpyxl")

print(df.columns.tolist())

# Renombrado inicial
renombres = {
    "RUC_CONSORCIO": "ruc_consorcio",
    "CONSORCIO": "nombre_consorcio",
    "RUC_INTEGRANTE": "ruc_integrante",
    "INTEGRANTE": "integrante",
    "PORCENTAJE_PARTICIPACION": "porcentaje_participacion"
}

for origen, destino in renombres.items():
    if origen in df.columns:
        df = df.rename(columns={origen: destino})

# Crear columnas si no existen
for col in [
    "ruc_consorcio",
    "nombre_consorcio",
    "ruc_integrante",
    "integrante",
    "porcentaje_participacion"
]:
    if col not in df.columns:
        df[col] = None

# Estructura final
df = df[
    [
        "ruc_consorcio",
        "nombre_consorcio",
        "ruc_integrante",
        "integrante",
        "porcentaje_participacion"
    ]
]

# Eliminar duplicados
df = df.drop_duplicates()

# Limpiar tabla
with engine.begin() as conn:
    conn.exec_driver_sql(
        "TRUNCATE TABLE fact_consorcio RESTART IDENTITY"
    )

# Cargar
df.to_sql(
    "fact_consorcio",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print("CONSORCIOS CARGADOS:", len(df))
