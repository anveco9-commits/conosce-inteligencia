import pandas as pd
from sqlalchemy import create_engine

# Conexión Neon
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_KUCFxuvDW46f@ep-red-cell-bdd49h0q-pooler.c-8.us-east-2.aws.neon.tech:5432/neondb?sslmode=require"
)

# Convocatorias Cajamarca
convocatorias = pd.read_sql(
    """
    SELECT
        codigo_convocatoria,
        entidad,
        descripcion_proceso,
        provincia_item,
        distrito_item
    FROM fact_convocatoria
    """,
    engine
)

# Archivo nulidades
url = "https://conosce.osce.gob.pe/buscador/assets/67ae6c4a/reportes/nulos/2026/NULOS2026_0.xlsx"

df = pd.read_excel(url, engine="openpyxl")

print(df.columns.tolist())

# Ajustar nombres
df = df.rename(columns={
    "CODIGOCONVOCATORIA": "codigo_convocatoria"
})

# Convertir
df["codigo_convocatoria"] = df["codigo_convocatoria"].astype(str)
convocatorias["codigo_convocatoria"] = convocatorias["codigo_convocatoria"].astype(str)

# Filtrar Cajamarca
df = df.merge(
    convocatorias,
    on="codigo_convocatoria",
    how="inner"
)

# Campos por defecto
if "causal_nulidad" not in df.columns:
    df["causal_nulidad"] = None

if "fecha_nulidad" not in df.columns:
    df["fecha_nulidad"] = None

# Estructura final
df = df[
    [
        "codigo_convocatoria",
        "entidad",
        "descripcion_proceso",
        "provincia_item",
        "distrito_item",
        "fecha_nulidad",
        "causal_nulidad"
    ]
]

# Limpiar tabla
with engine.begin() as conn:
    conn.exec_driver_sql(
        "TRUNCATE TABLE fact_nulidad RESTART IDENTITY"
    )

# Cargar
df.to_sql(
    "fact_nulidad",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000,
    method="multi"
)

print("NULIDADES CARGADAS:", len(df))
